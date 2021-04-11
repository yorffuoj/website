import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Station
from .forms import MapSizeForm
from .database_operations import refresh_database, reload_full_database, refresh

logger = logging.getLogger(__name__)


def index(request):
    logger.info("Loading main Velouse page")
    refresh_database()

    user = request.user
    if user.is_authenticated:
        form = MapSizeForm(
            initial={
                "lat": user.map_center.lat,
                "lng": user.map_center.lng,
                "zoom": user.map_zoom,
            }
        )
    else:
        form = MapSizeForm()

    context = {
        "stations": Station.objects.select_related("position").all(),
        "form": form,
    }
    return render(request, "velouse/index.html", context)


def update(request):
    reload_full_database()
    return HttpResponseRedirect(reverse("velouse:index"))


def set_default_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = MapSizeForm(request.POST)
            if form.is_valid():
                lat = form.cleaned_data["lat"]
                lng = form.cleaned_data["lng"]
                zoom = form.cleaned_data["zoom"]
                logger.info(
                    f"Set default view of {user.get_username()} to latitude {lat}, longitude {lng} and zoom {zoom}"
                )
                user.set_map_view(zoom, lat, lng)
                user.save()
                return HttpResponseRedirect(reverse("velouse:index"))
        else:
            form = MapSizeForm()
    return HttpResponseRedirect(reverse("velouse:index"))


def star(request, station_number):
    station = Station.objects.get(number=station_number)
    user = request.user
    if user.is_authenticated:
        user.toggle_station(station)
        user.save()
    return HttpResponseRedirect(reverse("velouse:index"))


def detail(request, station_number):
    station = Station.objects.get(number=station_number)
    logger.info(f'Loading information page for station "{station}"')
    refresh(station)
    context = {"station": station}
    return render(request, "velouse/detail.html", context)
