from django.urls import path

from . import views

app_name = 'velose'
urlpatterns = [
    path('', views.index, name='index'),
    path('update', views.update, name='update'),
    path('add', views.add, name='add'),
    path('<int:station_number>/remove', views.remove, name='remove'),
]
