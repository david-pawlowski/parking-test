from django.db import models
from django.utils import timezone
from django.forms import ValidationError

from parking.sensors import get_parking_spot_status
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


def validate_parking(parking) -> None:
    already_exists_count = ParkingSpotModel.objects.filter(
        parking=parking
    ).count()
    if already_exists_count == parking.capacity:
        raise ValidationError("Parking capacity exceeded.")


class ParkingModel(models.Model):
    name = models.CharField(max_length=64)
    latitude = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(0), MaxValueValidator(180)],
    )
    longitude = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(0), MaxValueValidator(180)],
    )
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f"Parking {self.name} with {self.capacity} slots."


class ParkingSpotModel(models.Model):
    number = models.CharField(max_length=32, unique=True)
    parking = models.ForeignKey(
        ParkingModel, on_delete=models.CASCADE, validators=[validate_parking]
    )
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

    def validate_unique(self):
        """
        This one is tricky as we override it only
        for checking uniquisity of number field in parking scope
        If model will be extended by different fields that should
        be unique globaly it will cause problems
        """
        qs = ParkingSpotModel.objects.filter(number=self.number)
        if qs.filter(parking=self.parking).exists():
            raise ValidationError("Number must be unique per parking.")


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
