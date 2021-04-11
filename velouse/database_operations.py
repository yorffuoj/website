import logging
import re

from .models import Station
from .jcdecaux_connexion import get_all_stations, get_station

logger = logging.getLogger(__name__)


def refresh_database():
    if not (all_db_stations := Station.objects.all()):
        reload_full_database()
    else:
        refresh_stations(all_db_stations)


def reload_full_database():
    logger.info(f"Update all the stations in database")
    Station.objects.all().delete()

    stations_list = create_stations_list()
    Station.objects.bulk_create(stations_list)
    logger.info(f"Station database updated")


def refresh_stations(db_stations):
    logger.info("Update station list")
    json_stations = {}
    for station in get_all_stations():
        json_stations.update({station.get("number"): station})

    for station in db_stations:
        api_station = json_stations.get(station.number)
        station.refresh(
            bike_stands=api_station.get("bike_stands"),
            available_bike_stands=api_station.get("available_bike_stands"),
            available_bikes=api_station.get("available_bikes"),
            status=api_station.get("status"),
            last_update=api_station.get("last_update"),
        )

    Station.objects.bulk_update(
        db_stations,
        fields=[
            "bike_stands",
            "available_bike_stands",
            "available_bikes",
            "status",
            "last_update",
        ],
    )
    logger.info("Stations database updated")


def create_stations_list():
    json_stations = get_all_stations()
    station_list = []
    for station in json_stations:
        new_name = extract_name(station.get("name"))
        db_station = Station.create(
            number=station.get("number"),
            contract_name=station.get("contract_name"),
            name=new_name,
            address=station.get("address"),
            position=station.get("position"),
            banking=station.get("banking"),
            bonus=station.get("bonus"),
            bike_stands=station.get("bike_stands"),
            available_bike_stands=station.get("available_bike_stands"),
            available_bikes=station.get("available_bikes"),
            status=station.get("status"),
            last_update=station.get("last_update"),
        )
        station_list.append(db_station)
    return station_list


def extract_name(name):
    """
    Extracts the real name of the station
    'ROQUELAINE' is extracted from '60 - ROQUELAINE'
    """
    p = re.compile(r"\d+ - ([\S\s]*)")
    return p.match(name).group(1).strip()


def refresh(station):
    logger.info(f"Refresh information for station {station}")
    json_station = get_station(station.number)
    station.refresh(
        bike_stands=json_station.get("bike_stands"),
        available_bike_stands=json_station.get("available_bike_stands"),
        available_bikes=json_station.get("available_bikes"),
        status=json_station.get("status"),
        last_update=json_station.get("last_update"),
    )
    station.save()
