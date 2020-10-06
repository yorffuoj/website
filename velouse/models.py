import json
from datetime import datetime

from django.db import models
from django.utils.timezone import make_aware
from django.contrib.auth.models import AbstractUser

STATION_STATUSES = (
    ('OPEN', 'Open'),
    ('CLOSED', 'Closed')
)


class Position(models.Model):
    lat = models.DecimalField(max_digits=17, decimal_places=14)
    lng = models.DecimalField(max_digits=17, decimal_places=14)

    @classmethod
    def create(cls, lat, lng):
        position = cls(lat=lat, lng=lng)
        return position

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Station(models.Model):
    number = models.IntegerField(primary_key=True)
    contract_name = models.CharField(max_length=50)
    name = models.CharField('nom', max_length=200)
    address = models.CharField('adresse', max_length=200)
    position = models.OneToOneField('Position', on_delete=models.CASCADE, null=True)
    banking = models.BooleanField()
    bonus = models.BooleanField()
    bike_stands = models.IntegerField('bornes')
    available_bike_stands = models.IntegerField('bornes dispos')
    available_bikes = models.IntegerField('velos dispos')
    status = models.CharField(max_length=200, choices=STATION_STATUSES)
    last_update = models.DateTimeField('dernière mise-à-jour')

    def __str__(self):
        return f"{self.number} - {self.name}"

    @classmethod
    def create(cls, number, contract_name, name, address, position, banking, bonus,
               bike_stands, available_bike_stands, available_bikes, status, last_update):
        position_do = Position.create(position.get('lat'), position.get('lng'))
        position_do.save()
        formatted_update = make_aware(datetime.fromtimestamp(last_update / 1000))
        station = cls(number=number,
                      contract_name=contract_name,
                      name=name,
                      address=address,
                      position=position_do,
                      banking=banking,
                      bonus=bonus,
                      bike_stands=bike_stands,
                      available_bike_stands=available_bike_stands,
                      available_bikes=available_bikes,
                      status=status,
                      last_update=formatted_update,
                      )
        return station

    def refresh(self, bike_stands, available_bike_stands, available_bikes, status, last_update):
        formatted_update = make_aware(datetime.fromtimestamp(last_update / 1000))
        self.bike_stands = bike_stands
        self.available_bike_stands = available_bike_stands
        self.available_bikes = available_bikes
        self.status = status
        self.last_update = formatted_update

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class VelouseUser(AbstractUser):
    stations = models.ManyToManyField(Station, blank=True)

    def toggle_station(self, station):
        if station in self.stations.all():
            self.stations.remove(station)
        else:
            self.stations.add(station)
