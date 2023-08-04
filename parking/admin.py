from django.contrib import admin
from .models import ParkingModel, ParkingSpotModel, ReservationModel, AvailabilityModel

# Register your models here.
admin.site.register(ParkingModel)
admin.site.register(ParkingSpotModel)
admin.site.register(ReservationModel)
admin.site.register(AvailabilityModel)
