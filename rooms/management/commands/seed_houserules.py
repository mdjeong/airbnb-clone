from django.core.management.base import BaseCommand
from rooms.models import HouseRule


class Command(BaseCommand):
    help = "this command that auto-create houserules"

    def handle(self, *args, **options):
        houserules = [
            "Not suitable for children and infants",
            "No smoking",
            "No pets",
            "No parties or events",
            "No laundry after p.m 9:00",
            "Security Deposits",
        ]

        for r in houserules:
            HouseRule.objects.create(name=r)

        self.stdout.write(self.style.SUCCESS("houserules Created!"))
