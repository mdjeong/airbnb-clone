import random
import datetime
from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker
from reservations.models import Reservation
from users.models import User
from rooms.models import Room

NAME = "reservations"


class Command(BaseCommand):
    help = f"this command create many {NAME}"

    def __init__(self):
        super().__init__()
        self._startday = datetime.datetime.now()

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

    def get_random_check_in(self):
        faker = Faker()
        start_day = datetime.date(year=2014, month=4, day=14)
        end_day = datetime.datetime.now() + datetime.timedelta(days=100)
        result = faker.date_between(start_day, end_day)
        self._startday = result
        return result

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder(locale=self._objlocale)
        rooms = Room.objects.all()
        users = User.objects.all()
        seeder.add_entity(
            Reservation,
            number,
            {
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: self.get_random_check_in(),
                "check_out": lambda x: self._startday
                + datetime.timedelta(days=random.randint(3, 25)),
            },
        )
        seeder.execute()

        self.stdout.write(
            self.style.SUCCESS(f"{self._objlocale} {number} {NAME} created!")
        )
