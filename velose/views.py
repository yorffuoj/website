import json
import math
import re
from datetime import datetime

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import AddStationForm
from .models import Station

STATIONS = [60, 35, 34, 97, ]
ADDED_STATIONS = []
BASE_URL = 'https://api.jcdecaux.com/vls/v1/stations/'
CONTRACT = 'toulouse'
API_KEY = '54b6f2be9a8f6d369691075425d0e11b4611a9d5'


def index(request):
    update_visible_stations()

    selected_stations = Station.objects.filter(number__in=STATIONS)
    added_stations = Station.objects.filter(number__in=ADDED_STATIONS)
    add_station_form = AddStationForm(displayed_stations=STATIONS + ADDED_STATIONS)

    context = {'selected_stations': selected_stations, 'added_stations': added_stations,
               'add_station_form': add_station_form}

    return render(request, 'velose/index.html', context)


def update_visible_stations():
    for station_nb in STATIONS + ADDED_STATIONS:
        station_url = f'{BASE_URL}{station_nb}?contract={CONTRACT}&apiKey={API_KEY}'
        updated_station = json.loads(requests.get(station_url).text)
        station = Station.objects.get(number=station_nb)
        station.refresh(updated_station.get('bike_stands'),
                        updated_station.get('available_bike_stands'),
                        updated_station.get('available_bikes'),
                        updated_station.get('status'),
                        updated_station.get('last_update'),
                        )
        station.save()


def update(request):
    update_database()
    compute_closest_stations()
    return HttpResponseRedirect(reverse('velose:index'))


def update_database():
    print(f'[{datetime.now()}] Start updating station database')
    print(f'[{datetime.now()}] Delete current database')
    Station.objects.all().delete()
    print(f'[{datetime.now()}] Request JCDecaux API')
    stations_url = f'{BASE_URL}?contract={CONTRACT}&apiKey={API_KEY}'
    req = requests.get(stations_url)
    stations = json.loads(req.text)
    for station in stations:
        print(f'[{datetime.now()}] Saving station {station.get("name")}')
        new_name = modify_name(station.get("name"))
        station.update({'name': new_name})
        static_station = Station.create(**station)
        static_station.save()
    print(f'[{datetime.now()}] Database updated')


def modify_name(name):
    p = re.compile("\d+ - ([\S\s]*)")
    return p.match(name).group(1).strip()


def compute_closest_stations():
    stations = Station.objects.all()
    positions = {}
    for station in stations:
        positions.update({station.number: station.position})
    for number1, position1 in positions.items():
        distances = {}
        for number2, position2 in positions.items():
            distances.update({number2: compute_distance(position1, position2)})
        closest_stations = [k for k, _ in sorted(distances.items(), key=lambda item: item[1])][1:6]

        print(f'closest stations of station {number1}: {closest_stations}')


def compute_distance(position1, position2):
    lat1 = position1.lat
    lat2 = position2.lat
    lng1 = position1.lng
    lng2 = position2.lng
    return math.sqrt((lat1 - lat2) * (lat1 - lat2) + (lng1 - lng2) * (lng1 - lng2))


def add(request):
    if request.GET:
        form = AddStationForm(request.GET, displayed_stations=STATIONS + ADDED_STATIONS)
        if form.is_valid():
            station = form.cleaned_data['stations']
            ADDED_STATIONS.append(station.number)
    return HttpResponseRedirect(reverse('velose:index'))


def remove(request, station_number):
    ADDED_STATIONS.remove(station_number)
    return HttpResponseRedirect(reverse('velose:index'))
