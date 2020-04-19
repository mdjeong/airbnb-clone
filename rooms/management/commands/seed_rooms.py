import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from faker import Faker
from rooms.models import (
    Room,
    RoomType,
    Photo,
    Amenity,
    Facility,
    HouseRule,
)

from users.models import User


class Command(BaseCommand):
    help = "this command create many rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="how many rooms do you want to create"
        )

    def get_random_locale_faker(self):
        locales = ["en_US", "ko_KR", "en_GB"]
        rd_local = random.choice(locales)
        faker = Faker(locale=rd_local)
        return faker

    def get_country(self, faker):
        c_dict = {
            "en_US": "US",
            "en_GB": "GB",
            "ko_KR": "KR",
        }
        key = faker._locales[0]
        # print(key)
        result = c_dict[key]
        # print(result)
        return result

    def handle(self, *args, **options):
        number = options.get("number")
        faker = self.get_random_locale_faker()
        seeder = Seed.seeder(locale=faker._locales[0])
        all_users = User.objects.all()
        all_roomtype = RoomType.objects.all()
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        rules = HouseRule.objects.all()
        seeder.add_entity(
            Room,
            number,
            {
                "name": lambda x: faker.catch_phrase(),
                "country": lambda x: self.get_country(faker),
                "city": lambda x: faker.city(),
                "description": lambda x: faker.paragraph(),
                "address": lambda x: faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(all_roomtype),
                "price": lambda x: random.randint(40, 1500),
                "guests": lambda x: random.randint(1, 60),
                "beds": lambda x: random.randint(1, 25),
                "bedrooms": lambda x: random.randint(1, 10),
                "baths": lambda x: random.randint(1, 4),
            },
        )
        ids_of_created_rooms = seeder.execute()
        clean_ids = flatten(list(ids_of_created_rooms.values()))

        for pk in clean_ids:
            room = Room.objects.get(pk=pk)
            for i in range(2, random.randint(5, 8)):
                Photo.objects.create(
                    caption=faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1,31)}.webp",
                )
            for a in amenities:
                magic_num = random.randint(0, 15)
                if magic_num % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_num = random.randint(0, 15)
                if magic_num % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_num = random.randint(0, 15)
                if magic_num % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(
            self.style.SUCCESS(f"{faker._locales[0]} {number} rooms created!")
        )
