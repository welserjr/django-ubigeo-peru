# -*- coding: utf-8 -*-

from django.forms import widgets
from .models import Ubigeo


class UbigeoWidget(widgets.MultiWidget):

    def __init__(self, regions, provinces, districts,
                 attrs_1=None, attrs_2=None, attrs_3=None, ):
        self.regions = regions
        self.provinces = provinces
        self.districts = districts
        _widgets = (
            widgets.Select(
                choices=self.regions,
                attrs=attrs_1,
            ),
            widgets.Select(
                choices=Ubigeo.objects.none(),
                attrs=attrs_2,
            ),
            widgets.Select(
                choices=Ubigeo.objects.none(),
                attrs=attrs_3,
            )
        )
        super(UbigeoWidget, self).__init__(_widgets)

    def decompress(self, value):
        """
        From the value stored in the DB it selects the fields and the choices
        for the select widget
        """
        if value:
            if isinstance(value, Ubigeo):
                value = value.pk
            ubigeo = Ubigeo.objects.get(pk=value)

            if ubigeo.human_political_division == 'Region':
                region_choices = [(u.pk, u.name) \
                                 for u in Ubigeo.objects.filter(
                            parent=ubigeo,
                            political_division=Ubigeo.PROVINCE)]
                region_choices.insert(0, (u'',''))  # Add null case
                self.widgets[1].choices = region_choices
                return (ubigeo.id,
                    None,
                    None)

            if ubigeo.human_political_division == 'Provincia':
                self.widgets[1].choices=((u.pk, u.name) \
                                 for u in Ubigeo.objects.filter(
                            parent=ubigeo.parent,
                            political_division=Ubigeo.PROVINCE))

                province_choices = [(u.pk, u.name) \
                                 for u in Ubigeo.objects.filter(
                            parent=ubigeo,
                            political_division=Ubigeo.DISTRICT)]
                province_choices.insert(0, (u'',''))  # Add null case
                self.widgets[2].choices=province_choices
                return (ubigeo.parent.id,
                    ubigeo.id,
                    None)

            if ubigeo.human_political_division == 'Distrito':
                self.widgets[1].choices=((u.pk, u.name) \
                                 for u in Ubigeo.objects.filter(
                            parent=ubigeo.parent.parent,
                            political_division=Ubigeo.PROVINCE))
                self.widgets[2].choices=((u.pk, u.name) \
                                 for u in Ubigeo.objects.filter(
                            parent=ubigeo.parent,
                            political_division=Ubigeo.DISTRICT))
                return (ubigeo.parent.parent.id,
                    ubigeo.parent.id,
                    ubigeo.id)
        return (None, None, None)
