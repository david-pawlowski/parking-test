import datetime
import pytz

from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User

from parameterized import parameterized

from parking.models import (
    AvailabilityModel,
    ParkingModel,
    ParkingSpotModel,
    ReservationModel,
)

# TODO: Rework test to actually check if validationerror was raised instead
# of checking assertingnotequal


class ParkingTests(APITestCase):
    def test_create_parking(self):
        url = reverse("parkings-list")
        data = {
            "name": "TestName",
            "latitude": 120,
            "longitude": 120,
            "capacity": 12,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingModel.objects.count(), 1)
        self.assertEqual(ParkingModel.objects.get().name, "TestName")

    @parameterized.expand(
        [
            None,
            190,
            -1,
        ]
    )
    def test_create_parking_fails_wrong_latitude(self, latitude):
        url = reverse("parkings-list")
        data = {
            "name": "TestName",
            "latitude": latitude,
            "longitude": 120,
            "capacity": 12,
        }
        response = self.client.post(url, data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(ParkingModel.objects.count(), 1)

    @parameterized.expand(
        [
            None,
            190,
            -1,
        ]
    )
    def test_create_parking_fails_wrong_longitude(self, longitude):
        url = reverse("parkings-list")
        data = {
            "name": "TestName",
            "latitude": 120,
            "longitude": longitude,
            "capacity": 12,
        }
        response = self.client.post(url, data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(ParkingModel.objects.count(), 1)

    @parameterized.expand(
        [
            None,
            0,
            -1,
        ]
    )
    def test_create_parking_fails_wrong_capacity(self, capacity):
        url = reverse("parkings-list")
        data = {
            "name": "TestName",
            "latitude": 120,
            "longitude": 130,
            "capacity": capacity,
        }
        response = self.client.post(url, data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(ParkingModel.objects.count(), 1)


class ParkingSpotTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", email="test@example.com", balance=12.0
        )
        self.parking = ParkingModel.objects.create(
            name="test", latitude=111, longitude=111, capacity=12
        )

    def test_create_parking_spot(self):
        url = reverse("spots-list")

        data = {
            "number": "Test1",
            "parking": self.parking.id,
            "owner": self.user.id,
            "occupied": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingSpotModel.objects.count(), 1)
        self.assertEqual(ParkingSpotModel.objects.get().number, "Test1")

    def test_create_parking_spot_fails_capacity_exceeded(self):
        url = reverse("spots-list")
        self.parking.capacity = 1
        self.parking.save()
        ParkingSpotModel.objects.create(
            number="Test1",
            parking=self.parking,
            owner=self.user,
            occupied=False,
        )
        data = {
            "number": "Test2",
            "parking": self.parking.id,
            "owner": self.user.id,
            "occupied": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(ParkingSpotModel.objects.get().number, "Test2")
        self.assertEqual(ParkingSpotModel.objects.count(), 1)
        self.assertEqual(ParkingSpotModel.objects.get().number, "Test1")

    def test_create_parking_spot_fails_same_spot_number_exists(self):
        url = reverse("spots-list")
        ParkingSpotModel.objects.create(
            number="Test1",
            parking=self.parking,
            owner=self.user,
            occupied=False,
        )
        data = {
            "number": "Test1",
            "parking": self.parking.id,
            "owner": self.user.id,
            "occupied": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(ParkingSpotModel.objects.get().number, "Test2")
        self.assertEqual(ParkingSpotModel.objects.count(), 1)
        self.assertEqual(ParkingSpotModel.objects.get().number, "Test1")


class ReservationTests(APITestCase):
    def test_create_reservation(self):
        url = reverse("reservations-list")
        user = User.objects.create(
            username="testuser", email="test@example.com", balance=12.0
        )
        parking = ParkingModel.objects.create(
            name="test", latitude=111, longitude=111, capacity=12
        )
        spot = ParkingSpotModel.objects.create(
            number="A1", parking=parking, owner=user, occupied=False
        )
        AvailabilityModel.objects.create(
            parking_spot=spot,
            available_from=timezone.now(),
            available_to=timezone.now() + datetime.timedelta(days=2),
            cost_per_hour=2,
        )
        data = {
            "reserved_by": user.id,
            "parking_spot": spot.id,
            "started_at": timezone.now(),
            "valid_until": timezone.now() + datetime.timedelta(days=1),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReservationModel.objects.count(), 1)
        parking_spot = ParkingSpotModel.objects.get(id=spot.id)
        self.assertTrue(parking_spot.occupied)

    def test_create_reservation_fails_parking_spot_occupied(self):
        url = reverse("reservations-list")
        user = User.objects.create(
            username="testuser", email="test@example.com", balance=12.0
        )
        parking = ParkingModel.objects.create(
            name="test", latitude=111, longitude=111, capacity=3
        )
        spot = ParkingSpotModel.objects.create(
            number="A1", parking=parking, owner=user, occupied=True
        )
        AvailabilityModel.objects.create(
            parking_spot=spot,
            available_from=timezone.now(),
            available_to=timezone.now() + datetime.timedelta(days=2),
            cost_per_hour=2,
        )
        data = {
            "reserved_by": user.id,
            "parking_spot": spot.id,
            "started_at": timezone.now(),
            "valid_until": timezone.now() + datetime.timedelta(days=1),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ReservationModel.objects.count(), 0)

    @parameterized.expand(
        [
            (
                timezone.now() + datetime.timedelta(days=1),
                timezone.now(),
                timezone.now() - datetime.timedelta(days=1),
                timezone.now() + datetime.timedelta(days=5),
            ),  # Start later than end
            (
                timezone.now(),
                timezone.now() + datetime.timedelta(days=1),
                timezone.now() + datetime.timedelta(hours=4),
                timezone.now() + datetime.timedelta(hours=6),
            ),  # Availible 4 hour after reservation starts
            (
                timezone.now() + datetime.timedelta(hours=4),
                timezone.now() + datetime.timedelta(days=1),
                timezone.now() + datetime.timedelta(days=1),
                timezone.now(),
            ),  # Availablity starts later than ends
            (
                timezone.now(),
                timezone.now() + datetime.timedelta(days=3),
                timezone.now() - datetime.timedelta(hours=4),
                timezone.now() + datetime.timedelta(days=2),
            ),  # Reservation ends later than availability
        ]
    )
    def test_create_reservation_fails_wrong_time_frame(
        self,
        reservation_starts,
        reservation_ends,
        availability_starts,
        availability_ends,
    ):
        url = reverse("reservations-list")
        user = User.objects.create(
            username="testuser", email="test@example.com", balance=12.0
        )
        parking = ParkingModel.objects.create(
            name="test", latitude=111, longitude=111, capacity=3
        )
        spot = ParkingSpotModel.objects.create(
            number="A1", parking=parking, owner=user, occupied=True
        )
        AvailabilityModel.objects.create(
            parking_spot=spot,
            available_from=availability_starts,
            available_to=availability_ends,
            cost_per_hour=2,
        )
        data = {
            "reserved_by": user.id,
            "parking_spot": spot.id,
            "started_at": reservation_starts,
            "valid_until": reservation_ends,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ReservationModel.objects.count(), 0)

    def test_calculate_total_cost(self):
        available_from = datetime.datetime(2023, 8, 10, 23, 0, 0, 0, pytz.UTC)
        available_to = datetime.datetime(2023, 8, 11, 23, 0, 0, 0, pytz.UTC)
        user = User.objects.create(
            username="testuser", email="test@example.com", balance=12.0
        )
        parking = ParkingModel.objects.create(
            name="test", latitude=111, longitude=111, capacity=12
        )
        spot = ParkingSpotModel.objects.create(
            number="A1", parking=parking, owner=user, occupied=False
        )
        AvailabilityModel.objects.create(
            parking_spot=spot,
            available_from=available_from,
            available_to=available_from + datetime.timedelta(days=2),
            cost_per_hour=1,
        )
        reservation = ReservationModel.objects.create(
            reserved_by=user,
            parking_spot=spot,
            started_at=available_from,
            valid_until=available_to,
        )
        self.assertEqual(reservation.total_cost, 24 * 1)


class AvailabilityTests(APITestCase):
    def test_split(self):
        available_from = datetime.datetime(2023, 8, 10, 23, 0, 0, 0, pytz.UTC)
        available_to = datetime.datetime(2023, 8, 16, 23, 0, 0, 0, pytz.UTC)
        user = User.objects.create(
            username="testuser", email="test@example.com", balance=12.0
        )
        parking = ParkingModel.objects.create(
            name="test", latitude=111, longitude=111, capacity=12
        )
        spot = ParkingSpotModel.objects.create(
            number="A1", parking=parking, owner=user, occupied=False
        )
        availability = AvailabilityModel.objects.create(
            parking_spot=spot,
            available_from=available_from,
            available_to=available_to,
            cost_per_hour=1,
        )
        split_start = datetime.datetime(2023, 8, 11, 23, 0, 0, 0, pytz.UTC)
        split_end = datetime.datetime(2023, 8, 12, 23, 0, 0, 0, pytz.UTC)
        self.assertEqual(AvailabilityModel.objects.count(), 1)
        availability.split(split_start, split_end)
        self.assertEqual(AvailabilityModel.objects.count(), 3)

