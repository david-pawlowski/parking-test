from rest_framework_nested import routers

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

# parking router
parking_router = routers.NestedSimpleRouter(
    router, r"parkings", lookup="parking"
)
parking_router.register(
    r"spots", views.ParkingSpotViewSet, basename="parking-spots"
)

#spot router
spot_router = routers.NestedSimpleRouter(
    parking_router, r"spots", lookup="spot"
)
spot_router.register(
    r"availabilities", views.AvailabilitySpotViewSet, basename="availabilities"
)
