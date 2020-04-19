from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):
    help = "this command that auto-create amenities"

    def handle(self, *args, **options):
        amenities = [
            "Bed sheets",
            "Body Cleanser",
            "Coffee Maker",
            "Dishes",
            "Facial Cleanser",
            "Hair Dryer",
            "Hangers",
            "Iron",
            "Lockbox",
            "Microwave",
            "Oil",
            "Pans",
            "Pepper",
            "Pots",
            "Salt",
            "Shampoo",
            "Silverware",
            "Soap",
            "Toilet Paper",
            "Towels",
        ]

        for a in amenities:
            Amenity.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("Amenities Created!"))
