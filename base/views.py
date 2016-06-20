# coding=UTF-8
import os

import time
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from geopy import Nominatim
from os import listdir
from os.path import isfile, join

from base.forms import MissionForm
from base.models import Mission, Training, BreathingProtectionTraining
from feumgmt import settings


class Dashboard(TemplateView):
    template_name = 'base/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(Dashboard, self).get_context_data(**kwargs)

        next_training = Training.objects.all().order_by('-date').first()
        ff = ','.join([str(f) for f in next_training.firefighters.all()])
        ctx['next_training'] = {
            'date': next_training.date,
            'subject': next_training.subject,
            'firefighters': ff,
        }

        next_bpt = BreathingProtectionTraining.objects.all().order_by('-date').first()
        ff = ','.join([str(f) for f in next_bpt.firefighters.all()])
        ctx['next_bpt'] = {
            'date': next_bpt.date,
            'location': next_bpt.location,
            'firefighters': ff,
        }

        return ctx


class MissionList(ListView):
    model = Mission


class MissionUpdate(UpdateView):
    model = Mission
    success_url = reverse_lazy('mission_list')
    form_class = MissionForm
    template_name = 'base/mission_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(MissionUpdate, self).get_context_data(**kwargs)

        geolocator = Nominatim(format_string="%s, Landkreis Sächsische Schweiz-Osterzgebirge, Sachsen, 01833, Deutschland")
        address = '{0}, {1}'.format(self.object.street, self.object.location)

        # 11, Alte Hauptstraße, Wilschdorf, Dürrröhrsdorf-Dittersbach, Landkreis Sächsische Schweiz-Osterzgebirge, Sachsen, 01833, Deutschland
        locations = geolocator.geocode(address, False)
        if locations:
            location = locations[0]
            ctx['address'] = location.address
            ctx['lat'] = float(location.latitude)
            ctx['long'] = float(location.longitude)
            ctx['raw'] = location.raw
        return ctx


class GalleryList(TemplateView):
    template_name = 'base/gallery_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(GalleryList, self).get_context_data(**kwargs)
        path = settings.MEDIA_ROOT + 'images/'
        files = []

        mtime = lambda f: os.stat(os.path.join(path, f)).st_ctime
        fls = list(sorted(os.listdir(path), key=mtime))
        index = 0
        for f in reversed(fls):
            index += 1
            file_path = join(path, f)
            if not isfile(file_path):
                continue
            files.append({
                'path': f,
                'time': time.ctime(os.path.getctime(file_path))
            })
            if index >= 15:
                break
        ctx['files'] = files
        return ctx
