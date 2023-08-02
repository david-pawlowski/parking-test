from django.db import models
from django.contrib.auth.models import User

from parking.sensors import get_parking_spot_status


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
    # Reservable in a way the owned want it to be reserved
    is_reservable = models.BooleanField(default=False)
    # join reservations
    # cost
    # exact place lat, long???
    # photo maybe

    @property
    def status(self):
        return get_parking_spot_status(self.number)

    def reserve(self):
        self.occupied = True
        self.save()
        # here we should make task to watch time until end of reservation. subscription

    def free_up(self):
        self.occupied = False
        self.save()
        # Delete task which is watching time

    
class ReservationModel(models.Model):
    reserved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_spot = models.ForeignKey(ParkingSpotModel, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now=True)
    valid_until = models.DateTimeField()
