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
from parking.tasks import send_email_task


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
        reserver_id = serializer.validated_data.get("reserved_by").email
        owner_id = serializer.validated_data.get("parking_spot").owner.email
        self.notify_users(reserver_id, owner_id)
        parking_spot.save()

    @staticmethod
    def notify_users(reserver_email, owner_email):
        title = "Your parking reservation!"
        owner_email_content = "leno paleno"
        reserver_email_content = "leno paleno"
        send_email_task.delay(title, reserver_email, reserver_email_content)
        send_email_task.delay(title, owner_email, owner_email_content)


class AvailabilitySpotViewSet(viewsets.ModelViewSet):
    queryset = AvailabilityModel.objects.select_related("parking_spot").all()
    serializer_class = AvailabilitySerializer
    permission_classess = []
