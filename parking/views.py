from rest_framework import viewsets
from parking.models import (
    AvailabilityModel,
    ParkingModel,
    ParkingSpotModel,
    ReservationModel,
)
from parking.serializers import (
    AvailabilitySerializer,
    ParkingSerializer,
    ParkingSpotSerializer,
    ReservationSerializer,
)


class ParkingViewSet(viewsets.ModelViewSet):
    queryset = ParkingModel.objects.all()
    serializer_class = ParkingSerializer
    permission_classess = []


class ParkingSpotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpotModel.objects.prefetch_related("availability").all()
    serializer_class = ParkingSpotSerializer
    permission_classess = []


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = ReservationModel.objects.all()
    serializer_class = ReservationSerializer
    permission_classess = []

    def perform_create(self, serializer):
        reservation = serializer.save()
        parking_spot = reservation.parking_spot
        # Actually here we need to start cron job
        # to check when reservation time ends
        # parking spot sensor data to determine if it is occupied
        # If it is start charging extra
        parking_spot.occupied = True
        parking_spot.save()


class AvailabilitySpotViewSet(viewsets.ModelViewSet):
    queryset = AvailabilityModel.objects.select_related("parking_spot").all()
    serializer_class = AvailabilitySerializer
    permission_classess = []
