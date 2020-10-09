from django.urls import path

from . import views

app_name = 'velouse'
urlpatterns = [
    path('', views.index, name='index'),
    path('update', views.update, name='update'),
    path('<int:station_number>/star', views.star, name='star'),
    path('<int:station_number>', views.detail, name='detail'),
]
