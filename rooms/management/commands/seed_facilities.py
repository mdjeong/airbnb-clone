from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "this command that auto-create facilities"

    def handle(self, *args, **options):
        facilities = [
            "Air Conditioner",
            "Air Purifier",
            "Audio System",
            "Carbon monoxide alarm",
            "Cleaner",
            "Fire extinguisher",
            "IPTV Box",
            "Indoor fireplace",
            "Lockbox",
            "Multiple Electrical Gagets Charger",
            "Oven",
            "Refrigerator",
            "Smoke alarm",
            "Stove",
            "TV",
            "Thermostat",
            "Washer",
            "Water Purifier",
            "WiFi",
        ]

        for f in facilities:
            Facility.objects.create(name=f)

        self.stdout.write(self.style.SUCCESS("facilities Created!"))
