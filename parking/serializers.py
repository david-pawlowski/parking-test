from django.forms import ValidationError
from rest_framework import serializers

import parking

from .models import (
    ParkingModel,
    ParkingSpotModel,
    ReservationModel,
    AvailabilityModel,
)
from accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class ParkingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParkingModel
        fields = ["name", "latitude", "longitude", "capacity"]


class AvailabilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AvailabilityModel
        fields = [
            "available_from",
            "available_to",
            "cost_per_hour",
            "parking_spot",
        ]


class ParkingSpotSerializer(serializers.ModelSerializer):
    availability = AvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = ParkingSpotModel
        fields = ["number", "parking", "owner", "occupied", "availability"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationModel
        fields = ["reserved_by", "parking_spot", "started_at", "valid_until"]

    def validate(self, attrs):
        # Calculate cost and check if user have sufficient balance
        parking_spot = attrs["parking_spot"]
        valid_until = attrs["valid_until"]
        if not parking_spot.is_available(valid_until):
            raise ValidationError(
                "Parking spot is not available for rent in provided time frame."
            )

        started_at = attrs["started_at"]
        reserved_by = attrs["reserved_by"]
        if reserved_by.balance < parking_spot.calculate_cost(
            started_at, valid_until
        ):
            raise ValidationError("User have unsufficient funds.")
        return super().validate(attrs)

    def validate_parking_spot(self, parking_spot):
        if parking_spot.occupied:
            raise ValidationError("Parking spot is currently occupied.")
        return parking_spot
