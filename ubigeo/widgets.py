# -*- coding: utf-8 -*-

from django.forms import widgets
from .models import Ubigeo


class UbigeoWidget(widgets.MultiWidget):

    def __init__(self, regions, provinces, districts):
        self.regions = regions
        self.provinces = provinces
        self.districts = districts
        _widgets = (
            widgets.Select(
                choices = self.regions,
                attrs = {'onchange' : 'getProvincias(this.value, null, null);'}
            ),
            widgets.Select(
                choices = Ubigeo.objects.none(),
                attrs = {'onchange' : 'getDistritos(this.value, null);'}
            ),
            widgets.Select(
                choices = Ubigeo.objects.none(),
            )
        )
        super(UbigeoWidget, self).__init__(_widgets)

    def decompress(self, value):
        if value:
            ubigeo = value if isinstance(value, Ubigeo) else Ubigeo.objects.get(
                ubigeo = value
                )
            self.widgets[1] = widgets.Select(
                choices=((u[0], u[1]) for u in self.provinces),
                attrs = {'onchange' : 'getDistritos(this.value);'}
                )
            self.widgets[2] = widgets.Select(
                choices = ((u[0], u[1]) for u in self.districts))
            return (ubigeo.parent.parent.ubigeo,
                ubigeo.parent.ubigeo,
                ubigeo.ubigeo)
        return (None, None, None)

    class Media:
        js=(
            'js/jquery.js',
            'js/ubigeo.js',
        )
