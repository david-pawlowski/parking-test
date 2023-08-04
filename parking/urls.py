from rest_framework import routers
from parking import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"parkings", views.ParkingViewSet)
router.register(r"spots", views.ParkingSpotViewSet)
router.register(r"reservations", views.ReservationViewSet)
