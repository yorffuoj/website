import json
import re
from datetime import datetime

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Station

BASE_URL = 'https://api.jcdecaux.com/vls/v1/stations/'
CONTRACT = 'toulouse'
API_KEY = '54b6f2be9a8f6d369691075425d0e11b4611a9d5'


def index(request):
    user = request.user
    refresh_database()
    starred_stations = user.stations.all() if user.is_authenticated else None

    context = {'starred_stations': starred_stations, 'stations': Station.objects.all(), }

    return render(request, 'velouse/index.html', context)


def refresh_station(station_nb):
    station_url = f'{BASE_URL}{station_nb}?contract={CONTRACT}&apiKey={API_KEY}'
    json_station = json.loads(requests.get(station_url).text)
    db_station = Station.objects.get(number=station_nb)
    db_station.refresh(bike_stands=json_station.get('bike_stands'),
                       available_bike_stands=json_station.get('available_bike_stands'),
                       available_bikes=json_station.get('available_bikes'),
                       status=json_station.get('status'),
                       last_update=json_station.get('last_update'),
                       )
    db_station.save()


def update(request):
    reload_full_database()
    return HttpResponseRedirect(reverse('velouse:index'))


def get_stations_from_api():
    stations_url = f'{BASE_URL}?contract={CONTRACT}&apiKey={API_KEY}'
    req = requests.get(stations_url)
    return json.loads(req.text)


def reload_full_database():
    print(f'[{datetime.now()}] Start updating station database')
    print(f'[{datetime.now()}] Delete current database')
    Station.objects.all().delete()
    json_stations = get_stations_from_api()
    print(f'[{datetime.now()}] Create station list')
    station_list = []
    for station in json_stations:
        new_name = modify_name(station.get('name'))
        db_station = Station.create(
            number=station.get('number'),
            contract_name=station.get('contract_name'),
            name=new_name,
            address=station.get('address'),
            position=station.get('position'),
            banking=station.get('banking'),
            bonus=station.get('bonus'),
            bike_stands=station.get('bike_stands'),
            available_bike_stands=station.get('available_bike_stands'),
            available_bikes=station.get('available_bikes'),
            status=station.get('status'),
            last_update=station.get('last_update')
        )
        station_list.append(db_station)

    print(f'[{datetime.now()}] Start bulk create')
    Station.objects.bulk_create(station_list)
    print(f'[{datetime.now()}] Database updated')


def refresh_database():
    if not Station.objects.all():
        reload_full_database()

    stations = get_stations_from_api()
    station_list = []
    for station in stations:
        database_station = Station.objects.get(number=station.get('number'))
        database_station.refresh(bike_stands=station.get('bike_stands'),
                                 available_bike_stands=station.get('available_bike_stands'),
                                 available_bikes=station.get('available_bikes'),
                                 status=station.get('status'),
                                 last_update=station.get('last_update'))
        station_list.append(database_station)

    Station.objects.bulk_update(station_list,
                                fields=['bike_stands', 'available_bike_stands', 'available_bikes', 'status',
                                        'last_update'])


def modify_name(name):
    p = re.compile("\d+ - ([\S\s]*)")
    return p.match(name).group(1).strip()


def star_no_arg(request):
    if request.POST:
        station_number = request.POST.get('station')
    return star(request, station_number)


def star(request, station_number):
    station = Station.objects.get(number=station_number)
    user = request.user
    if user.is_authenticated:
        user.toggle_station(station)
        user.save()
    return HttpResponseRedirect(reverse('velouse:index'))


def detail(request, station_number):
    refresh_station(station_number)
    context = {'station': Station.objects.get(number=station_number)}
    return render(request, 'velouse/detail.html', context)
