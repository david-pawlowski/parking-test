from django.forms import ValidationError
from rest_framework import serializers
from .models import ParkingModel, ParkingSpotModel, ReservationModel
from accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class ParkingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParkingModel
        fields = ["name", "latitude", "longitude", "capacity"]


class ParkingSpotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParkingSpotModel
        fields = ["number", "parking", "owner", "occupied", "is_reservable"]


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReservationModel
        fields = ["reserved_by", "parking_spot", "started_at", "valid_until"]

    def validate_parking_spot(self, parking_spot):
        if not parking_spot.is_reservable:
            raise ValidationError("This spot is not available for reservation.")
        if parking_spot.occupied:
            raise ValidationError("Parking spot is currently occupied.")
        return parking_spot
