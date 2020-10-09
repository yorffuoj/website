import json
import re
import logging

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Station, Position

BASE_URL = 'https://api.jcdecaux.com/vls/v1/stations/'
CONTRACT = 'toulouse'
API_KEY = '54b6f2be9a8f6d369691075425d0e11b4611a9d5'

logger = logging.getLogger(__name__)


def index(request):
    logger.info('Loading main Velouse page')
    refresh_database()
    context = {'stations': Station.objects.select_related('position').all()}
    return render(request, 'velouse/index.html', context)


def refresh_database():
    all_db_stations = Station.objects.all()
    if not all_db_stations:
        reload_full_database()
    else:
        refresh_stations(all_db_stations)


def reload_full_database():
    logger.info(f'Reload all the database')
    Station.objects.all().delete()
    json_stations = get_stations_from_api()
    logger.info(f'Create station list')
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

    logger.info(f'Save all stations in database')
    Station.objects.bulk_create(station_list)
    logger.info(f'Database update done')


def get_stations_from_api():
    logger.info('Request stations to JCDecaux API')
    stations_url = f'{BASE_URL}?contract={CONTRACT}&apiKey={API_KEY}'
    req = requests.get(stations_url)
    return json.loads(req.text)


def modify_name(name):
    p = re.compile("\d+ - ([\S\s]*)")
    return p.match(name).group(1).strip()


def refresh_stations(db_stations):
    json_stations = {}
    for station in get_stations_from_api():
        json_stations.update({station.get('number'): station})

    logger.info('Update station list')
    for station in db_stations:
        api_station = json_stations.get(station.number)
        station.refresh(bike_stands=api_station.get('bike_stands'),
                        available_bike_stands=api_station.get('available_bike_stands'),
                        available_bikes=api_station.get('available_bikes'),
                        status=api_station.get('status'),
                        last_update=api_station.get('last_update'))

    logger.info('Save updated stations to database')
    Station.objects.bulk_update(db_stations,
                                fields=['bike_stands', 'available_bike_stands', 'available_bikes', 'status',
                                        'last_update'])


def update(request):
    reload_full_database()
    return HttpResponseRedirect(reverse('velouse:index'))


def set_default_view(request, zoom, latitude, longitude):
    user = request.user
    if user.is_authenticated:
        logger.info(f'Set default view of {user.get_username()} to latitude {latitude}, longitude {longitude}'
                    f' and zoom {zoom}')
        user.set_map_view(zoom, latitude, longitude)
        user.save()
    return HttpResponseRedirect(reverse('velouse:index'))


def star(request, station_number):
    station = Station.objects.get(number=station_number)
    user = request.user
    if user.is_authenticated:
        user.toggle_station(station)
        user.save()
    return HttpResponseRedirect(reverse('velouse:index'))


def detail(request, station_number):
    station = Station.objects.get(number=station_number)
    logger.info('Loading information page for station "{station}"')
    refresh(station)
    context = {'station': station}
    return render(request, 'velouse/detail.html', context)


def refresh(station):
    logger.info(f'Refresh information for station {station}')
    station_nb = station.number
    station_url = f'{BASE_URL}{station_nb}?contract={CONTRACT}&apiKey={API_KEY}'
    json_station = json.loads(requests.get(station_url).text)
    station.refresh(bike_stands=json_station.get('bike_stands'),
                    available_bike_stands=json_station.get('available_bike_stands'),
                    available_bikes=json_station.get('available_bikes'),
                    status=json_station.get('status'),
                    last_update=json_station.get('last_update'),
                    )
    station.save()
