import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from users.models import User
from rooms.models import Room

NAME = "lists"


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
            List, number, {"user": lambda x: random.choice(users),},
        )
        created_lists = seeder.execute()
        pure_ids = flatten(created_lists.values())
        for pk in pure_ids:
            r_list = List.objects.get(pk=pk)

            for r in rooms:
                mg_num = random.randint(0, 15)
                if mg_num % 2 == 0:
                    r_list.rooms.add(r)

        self.stdout.write(
            self.style.SUCCESS(f"{self._objlocale} {number} {NAME} created!")
        )
