# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

import time
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView
from geopy import Nominatim
from os import listdir
from os.path import isfile, join

from base.forms import MissionForm, BPTrainingForm
from base.models import Mission, Training, BreathingProtectionTraining
from feumgmt import settings


class Dashboard(TemplateView):
    template_name = 'base/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(Dashboard, self).get_context_data(**kwargs)

        next_training = Training.objects.all().order_by('-date').first()
        if next_training:
            responsibles = ','.join([str(f) for f in next_training.responsibles.all()])
            ctx['next_training'] = {
                'date': next_training.date,
                'subject': next_training.subject,
                'responsibles': responsibles,
            }

        next_bpt = BreathingProtectionTraining.objects.all().order_by('-date').first()
        if next_bpt:
            participants = ','.join([str(f) for f in next_bpt.participants.all()])
            ctx['next_bpt'] = {
                'date': next_bpt.date,
                'location': next_bpt.location,
                'participants': participants,
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


class BPTrainingList(ListView):
    model = BreathingProtectionTraining
    template_name = 'base/bptraining_list.html'


class BPTrainingCreate(CreateView):
    model = BreathingProtectionTraining
    success_url = reverse_lazy('bptraining_list')
    form_class = BPTrainingForm
    template_name = 'base/bptraining_form.html'


class BPTrainingUpdate(UpdateView):
    model = BreathingProtectionTraining
    success_url = reverse_lazy('bptraining_list')
    form_class = BPTrainingForm
    template_name = 'base/bptraining_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(BPTrainingUpdate, self).get_context_data(**kwargs)
        # todo
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
