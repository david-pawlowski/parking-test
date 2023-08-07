from django.forms import ValidationError
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User

from parameterized import parameterized

from parking.models import ParkingModel, ParkingSpotModel

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
        self.assertRaises(ValidationError)
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
    def test_create_parking_spot(self):
        url = reverse("spots-list")
        user = User.objects.create(
            username="testuser", email="test@example.com", balance=12.0
        )
        parking = ParkingModel.objects.create(
            name="test", latitude=111, longitude=111, capacity=12
        )
        data = {
            "number": "Test1",
            "parking": parking.id,
            "owner": user.id,
            "occupied": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingSpotModel.objects.count(), 1)
        self.assertEqual(ParkingSpotModel.objects.get().number, "Test1")

    def test_create_parking_spot_fails_capacity_exceeded(self):
        url = reverse("spots-list")
        user = User.objects.create(
            username="testuser", email="test@example.com", balance=12.0
        )
        parking = ParkingModel.objects.create(
            name="test", latitude=111, longitude=111, capacity=1
        )
        ParkingSpotModel.objects.create(
            number="Test1", parking=parking, owner=user, occupied=False
        )
        data = {
            "number": "Test2",
            "parking": parking.id,
            "owner": user.id,
            "occupied": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(ParkingSpotModel.objects.get().number, "Test2")
        self.assertEqual(ParkingSpotModel.objects.count(), 1)
        self.assertEqual(ParkingSpotModel.objects.get().number, "Test1")

    def test_create_parking_spot_fails_same_spot_number_exists(self):
        url = reverse("spots-list")
        user = User.objects.create(
            username="testuser", email="test@example.com", balance=12.0
        )
        parking = ParkingModel.objects.create(
            name="test", latitude=111, longitude=111, capacity=3
        )
        ParkingSpotModel.objects.create(
            number="Test1", parking=parking, owner=user, occupied=False
        )
        data = {
            "number": "Test1",
            "parking": parking.id,
            "owner": user.id,
            "occupied": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(ParkingSpotModel.objects.get().number, "Test2")
        self.assertEqual(ParkingSpotModel.objects.count(), 1)
        self.assertEqual(ParkingSpotModel.objects.get().number, "Test1")