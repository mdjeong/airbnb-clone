from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """

    list_display = ["__str__", "get_thumbnail"]

    def get_thumbnail(self, obj):
        return mark_safe(f"<img width='200px' src='{obj.file.url}' />'")

    get_thumbnail.short_description = "thumbnail"


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = [
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")},),
        (
            "More About the Spaces",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules",),
            },
        ),
        ("Last Details", {"fields": ("host",)},),
    ]

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "total_rating",
        "count_amenities",
        "count_photos",
    )

    ordering = ("name", "price", "bedrooms")

    list_filter = (
        "instant_book",
        "host__superhost",
        "host__gender",
        "room_type",
        "city",
        "amenities",
        "facilities",
        "house_rules",
        "country",
    )

    filter_horizontal = ("amenities", "facilities", "house_rules")

    raw_id_fields = ("host",)

    search_fields = ("city", "host__username")

    def count_amenities(self, obj):
        result = f"{obj.amenities.count()}"
        return result

    def count_photos(self, obj):
        return f"{obj.photos.count()}"

    count_amenities.short_description = "Count Amenities"
    count_photos.short_description = "Count Photos"
