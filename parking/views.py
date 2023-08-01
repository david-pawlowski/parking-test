from django.contrib.auth.models import User, Group
from parking.models import ParkingModel, ParkingSpotModel, ReservationModel
from rest_framework import viewsets
from rest_framework import permissions
from parking.serializers import UserSerializer, GroupSerializer, ParkingSerializer, ParkingSpotSerializer, ReservationSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ParkingViewSet(viewsets.ModelViewSet):
    queryset = ParkingModel.objects.all()
    serializer_class = ParkingSerializer
    permission_classess = []


class ParkingSpotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpotModel.objects.all()
    serializer_class = ParkingSpotSerializer
    permission_classess = []


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = ReservationModel.objects.all()
    serializer_class = ReservationSerializer
    permission_classess = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return super().create(request, *args, **kwargs)