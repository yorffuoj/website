from django import forms

from .models import Station


class AddStationForm(forms.Form):
    stations = forms.ModelChoiceField(queryset=Station.objects.all().order_by('name'),
                                      to_field_name='name',
                                      empty_label='Choisir une station',
                                      label='Ajouter une station',
                                      label_suffix=' : ',
                                      )

    def __init__(self, *args, **kwargs):
        displayed_stations = kwargs.pop('displayed_stations', None)
        super(AddStationForm, self).__init__(*args, **kwargs)
        self.fields['stations'].queryset = Station.objects.exclude(number__in=displayed_stations).order_by('name')
