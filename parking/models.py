from django.db import models
from django.utils import timezone

from parking.sensors import get_parking_spot_status
from accounts.models import User


class ParkingModel(models.Model):
    name = models.CharField(max_length=64)
    latitude = models.DecimalField(decimal_places=2, max_digits=5)
    longitude = models.DecimalField(decimal_places=2, max_digits=5)
    capacity = models.IntegerField()

    def __str__(self) -> str:
        return f"Parking {self.name} with {self.capacity} slots."


class ParkingSpotModel(models.Model):
    number = models.CharField(max_length=32)
    parking = models.ForeignKey(ParkingModel, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    occupied = models.BooleanField(default=False)
    # exact place lat, long???
    # photo maybe

    def __str__(self) -> str:
        return f"Spot {self.number} on {self.parking.name} \
            currently {'not' if not self.occupied else ''} occupied"

    @property
    def status(self):
        return get_parking_spot_status(self.number)

    def is_available(self, end_of_reservation):
        now = timezone.now()
        for availability in self.availability.all():
            if (
                availability.available_from < now
                and availability.available_to > end_of_reservation
            ):
                return True
        return False

    def reserve(self):
        self.occupied = True
        self.save()
        # here we should make task to watch
        # time until end of reservation. subscription

    def free_up(self):
        self.occupied = False
        self.save()
        # Delete task which is watching time


class AvailabilityModel(models.Model):
    parking_spot = models.ForeignKey(
        ParkingSpotModel, on_delete=models.CASCADE, related_name="availability"
    )
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()
    cost_per_hour = models.DecimalField(decimal_places=2, max_digits=4)


class ReservationModel(models.Model):
    reserved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(
        ParkingSpotModel, on_delete=models.CASCADE
    )
    started_at = models.DateTimeField(auto_now=True)
    valid_until = models.DateTimeField()
