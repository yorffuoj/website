from django import forms
from django.conf import settings

LABEL_SUFFIX = ''


class MapSizeForm(forms.Form):
    lat = forms.FloatField(required=True,
                           initial=settings.DEFAULT_LATITUDE,
                           label='Latitude',
                           label_suffix=LABEL_SUFFIX,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           )
    lng = forms.FloatField(required=True,
                           initial=settings.DEFAULT_LONGITUDE,
                           label='Longitude',
                           label_suffix=LABEL_SUFFIX,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           )
    zoom = forms.IntegerField(required=False,
                              initial=settings.DEFAULT_ZOOM,
                              label='Zoom',
                              label_suffix=LABEL_SUFFIX,
                              widget=forms.TextInput(attrs={'class': 'form-control'}),
                              )
