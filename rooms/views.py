# from django.utils import timezone
from django.shortcuts import render, redirect

# from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView
from django_countries import countries
from . import models


class HomeView(ListView):

    """ HomeView Class Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    page_kwarg = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # now = timezone.now()
        # context["now"] = now
        return context


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


# HomeView (Generic ListView)와 동일
def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()  # queryset
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"pages": rooms})
    except EmptyPage:
        return redirect("/")


# RoomDetail (Generic DetailView)와 동일
def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        raise Http404()


# RoomSearch (Generic SearchView)와 동일
def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 1))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    super_host = bool(request.GET.get("super_host", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "instant": instant,
        "super_host": super_host,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}
    if city != "Anywhere":
        filter_args["city__startswith"] = city
    filter_args["country"] = country
    if room_type != 0:
        filter_args["room_type__pk"] = room_type
    if price != 0:
        filter_args["price__lte"] = price
    if guests != 0:
        filter_args["guests__gte"] = guests
    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms
    if beds != 0:
        filter_args["beds__gte"] = beds
    if baths != 0:
        filter_args["baths__gte"] = baths
    if instant:
        filter_args["instant_book"] = True
    if super_host:
        filter_args["host__superhost"] = True
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)
    if len(s_facilities) > 0:
        for f_facility in s_facilities:
            filter_args["facilities__pk"] = int(f_facility)

    rooms = models.Room.objects.filter(**filter_args)  # search result

    return render(
        request, "rooms/search.html", context={**form, **choices, "rooms": rooms},
    )
