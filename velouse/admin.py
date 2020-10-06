from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Station, Position, VelouseUser


class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'bike_stands', 'available_bikes', 'available_bike_stands')


class VelouseUserAdmin(UserAdmin):
    ...
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('stations',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('stations',)}),
    )


admin.site.register(Station, StationAdmin)
admin.site.register(Position)
admin.site.register(VelouseUser, VelouseUserAdmin)
