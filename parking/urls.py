from rest_framework import routers

from parking import views

router = routers.DefaultRouter()
router.register(r"parkings", views.ParkingViewSet, basename="parkings")
router.register(r"spots", views.ParkingSpotViewSet, basename="spots")
router.register(
    r"reservations", views.ReservationViewSet, basename="reservations"
)
router.register(
    r"spots-availabilities",
    views.AvailabilitySpotViewSet,
    basename="spots-availabilities",
)
