from django.core.management.base import BaseCommand
from django.utils import timezone

from parking.models import ParkingSpotModel

class Command(BaseCommand):
    help = "Updates occupied status of parking spots"

    def handle(self, *args, **options):
        # TODO: Sensor data
        ParkingSpotModel.objects.filter(availability__available_to__lte=timezone.now()).update(occupied=False)
        self.stdout.write(self.style.SUCCESS('Successfully updated occupied status of parking spots'))
