import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from users.models import User
from rooms.models import Room

NAME = "reviews"


class Command(BaseCommand):
    help = f"this command create many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"how many {NAME} do you want to create",
        )

    @property
    def _objlocale(self):
        locales = ["en_US", "ko_KR", "en_GB"]
        rd_local = random.choice(locales)
        return rd_local

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder(locale=self._objlocale)
        # faker = self.get_random_locale_faker()
        rooms = Room.objects.all()
        users = User.objects.all()
        seeder.add_entity(
            Review,
            number,
            {
                "accuracy": lambda x: random.randint(0, 5),
                "communication": lambda x: random.randint(0, 5),
                "cleanliness": lambda x: random.randint(0, 5),
                "location": lambda x: random.randint(0, 5),
                "check_in": lambda x: random.randint(0, 5),
                "value": lambda x: random.randint(0, 5),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )
        seeder.execute()
        self.stdout.write(
            self.style.SUCCESS(f"{self._objlocale} {number} {NAME} created!")
        )
