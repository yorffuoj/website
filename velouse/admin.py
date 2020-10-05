from django.contrib import admin

from .models import Station, Position


class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'bike_stands', 'available_bikes', 'available_bike_stands')


admin.site.register(Station, StationAdmin)
admin.site.register(Position)
