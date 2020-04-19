from django.core.management.base import BaseCommand
from rooms.models import RoomType


class Command(BaseCommand):
    help = "this command that auto-create roomtypes"

    def handle(self, *args, **options):

        space = [
            "Entire",
            "Shared",
            "Private",
        ]
        types = [
            "House",
            "Hotel",
            "Condominium",
            "Apartment",
            "Room",
            "Guesthouse",
            "Cottage",
        ]
        roomtypes = list(f"{sp} {tp}" for sp in space for tp in types)

        for rt in roomtypes:
            RoomType.objects.create(name=rt)

        self.stdout.write(self.style.SUCCESS("roomtypes Created!"))
