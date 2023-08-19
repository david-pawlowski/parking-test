from rest_framework import viewsets
from accounts.models import User
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
from parking.tasks import send_reservation_mail


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
        user_email = User.objects.get(
            pk=serializer.validated_data.get("reserved_by")
        ).email
        email_content = "leno paleno"
        send_reservation_mail.delay(user_email, email_content)
        parking_spot.occupied = True
        parking_spot.save()


class AvailabilitySpotViewSet(viewsets.ModelViewSet):
    queryset = AvailabilityModel.objects.select_related("parking_spot").all()
    serializer_class = AvailabilitySerializer
    permission_classess = []
