from django.forms import ValidationError
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from parameterized import parameterized

from parking.models import ParkingModel


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
