from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ParkingModel, ParkingSpotModel, ReservationModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


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
