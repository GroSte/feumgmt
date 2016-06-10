# coding=UTF-8
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from geopy import Nominatim

from base.forms import MissionForm
from base.models import Mission


class Dashboard(TemplateView):
    template_name = 'base/dashboard.html'


class MissionList(ListView):
    model = Mission


class MissionUpdate(UpdateView):
    model = Mission
    success_url = reverse_lazy('mission_list')
    form_class = MissionForm
    template_name = 'base/mission_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(MissionUpdate, self).get_context_data(**kwargs)

        geolocator = Nominatim()
        address = '{0} {1}'.format(self.object.street, self.object.location)
        location = geolocator.geocode(address)

        if location:
            ctx['address'] = location.address
            ctx['lat'] = location.latitude
            ctx['long'] = location.longitude
            ctx['raw'] = location.raw
        return ctx
