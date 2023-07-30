from django.db import models

# Create your models here.
class Parking(models.Model):
    name = models.CharField(max_length=64)
    latitude = models.DecimalField(decimal_places=8, max_digits=180)
    longitude = models.DecimalField(decimal_places=8, max_digits=180)
    capacity = models.IntegerField()


class ParkingSpot(models.Model):
    number = models.CharField(max_length=32)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    owner = models.CharField(max_length=16) # Charfield for now
    occupied = models.BooleanField(default=False)
    is_reservable = models.BooleanField(default=False)
    # join reservations
    # cost
    # exact place lat, long???
    # photo maybe
    