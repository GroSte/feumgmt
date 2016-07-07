# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.encoding import force_text
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from os.path import isfile, join

from base.forms import MissionForm, BPTrainingForm, MessageForm, BPCarrierForm, TrainingForm, \
    UserPasswordChangeForm
from base.geo_locator import GeoLocator
from base.importer import UserImporter, TrainingImporter
from base.models import Mission, Training, BreathingProtectionTraining, Message, UserProfile
from feumgmt import settings


class Dashboard(TemplateView):
    template_name = 'base/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(Dashboard, self).get_context_data(**kwargs)

        try:
            next_training = Training.objects.filter(date__gt=timezone.now()).order_by(
                'date').first()
            responsibles = ', '.join([unicode(f) for f in next_training.responsibles.all()])
            ctx['next_training'] = {
                'date': next_training.date,
                'subject': next_training.subject,
                'responsibles': responsibles,
            }
        except ObjectDoesNotExist:
            ctx['next_training'] = None

        try:
            next_bpt = BreathingProtectionTraining.objects.filter(
                date__gt=timezone.now()).order_by('date').first()
            participants = ', '.join([unicode(f) for f in next_bpt.participants.all()])
            ctx['next_bpt'] = {
                'date': next_bpt.date,
                'location': next_bpt.location,
                'participants': participants,
            }
        except ObjectDoesNotExist:
            ctx['next_bpt'] = None

        ctx['next_birthdays'] = UserProfile.get_next_birthdays()

        next_messages = Message.objects.all().order_by('-creation_date')[:3]
        if next_messages:
            ctx['next_messages'] = next_messages

        return ctx


class UserChangePassword(LoginRequiredMixin, FormView):
    success_url = reverse_lazy('logout')
    form_class = UserPasswordChangeForm
    template_name = 'base/user_change_password.html'

    def get_form_kwargs(self):
        kwargs = super(UserChangePassword, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UserChangePassword, self).form_valid(form)


class MissionList(ListView):
    model = Mission


class MissionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mission
    success_url = reverse_lazy('mission_list')
    form_class = MissionForm
    template_name = 'base/mission_form.html'
    permission_required = 'base.add_mission'

    def form_valid(self, form):
        form.instance.organizer_id = self.request.user.id
        form.instance.editor_id = self.request.user.id
        form.instance.creation_date = timezone.now()
        return super(MissionCreate, self).form_valid(form)


class MissionUpdate(UpdateView):
    model = Mission
    success_url = reverse_lazy('mission_list')
    form_class = MissionForm
    template_name = 'base/mission_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(MissionUpdate, self).get_context_data(**kwargs)

        geo_locator = GeoLocator()
        key = settings.MAP_QUEST_KEY
        address = '{0}, {1}'.format(self.object.street, self.object.location)

        ctx.update(geo_locator.get_location_coordinates(key, address))
        ctx.update(geo_locator.get_route(key, address))
        return ctx


class MissionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mission
    success_url = reverse_lazy('mission_list')
    template_name = 'base/_confirm_delete.html'
    permission_required = 'base.delete_mission'

    def get_context_data(self, **kwargs):
        ctx = super(MissionDelete, self).get_context_data(**kwargs)
        ctx['object_primary_name'] = getattr(self.get_object(), 'description')
        ctx['object_secondary_name'] = getattr(self.get_object(), 'alarm_time')
        ctx['object_class_name'] = force_text(self.model._meta.verbose_name)
        return ctx


class MissionAlarm(TemplateView):
    model = Mission
    template_name = 'base/mission_alarm.html'

    def get_context_data(self, **kwargs):
        ctx = super(MissionAlarm, self).get_context_data(**kwargs)
        mission = Mission.objects.get(pk=self.kwargs.get('pk'))
        ctx['object'] = mission

        geo_locator = GeoLocator()
        key = settings.MAP_QUEST_KEY
        address = '{0}, {1}'.format(mission.street, mission.location)

        ctx.update(geo_locator.get_location_coordinates(key, address))
        ctx.update(geo_locator.get_route(key, address))
        return ctx


class BPTrainingList(ListView):
    model = BreathingProtectionTraining
    template_name = 'base/bptraining_list.html'


class BPTrainingCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BreathingProtectionTraining
    success_url = reverse_lazy('bptraining_list')
    form_class = BPTrainingForm
    template_name = 'base/bptraining_form.html'
    permission_required = 'base.add_breathingprotectiontraining'

    def form_valid(self, form):
        form.instance.organizer_id = self.request.user.id
        form.instance.editor_id = self.request.user.id
        form.instance.creation_date = timezone.now()
        return super(BPTrainingCreate, self).form_valid(form)


class BPTrainingUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BreathingProtectionTraining
    success_url = reverse_lazy('bptraining_list')
    form_class = BPTrainingForm
    template_name = 'base/bptraining_form.html'
    permission_required = 'base.change_breathingprotectiontraining'

    def form_valid(self, form):
        form.instance.editor_id = self.request.user.id
        return super(BPTrainingUpdate, self).form_valid(form)


class BPTrainingDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BreathingProtectionTraining
    success_url = reverse_lazy('bptraining_list')
    template_name = 'base/_confirm_delete.html'
    permission_required = 'base.delete_breathingprotectiontraining'

    def get_context_data(self, **kwargs):
        ctx = super(BPTrainingDelete, self).get_context_data(**kwargs)
        ctx['object_primary_name'] = getattr(self.get_object(), 'date')
        ctx['object_secondary_name'] = getattr(self.get_object(), 'location')
        ctx['object_class_name'] = force_text(self.model._meta.verbose_name)
        return ctx


class TrainingList(ListView):
    model = Training
    template_name = 'base/training_list.html'


class TrainingCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Training
    success_url = reverse_lazy('training_list')
    form_class = TrainingForm
    template_name = 'base/training_form.html'
    permission_required = 'base.add_training'

    def form_valid(self, form):
        form.instance.organizer_id = self.request.user.id
        form.instance.editor_id = self.request.user.id
        form.instance.creation_date = timezone.now()
        return super(TrainingCreate, self).form_valid(form)


class TrainingUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Training
    success_url = reverse_lazy('training_list')
    form_class = TrainingForm
    template_name = 'base/training_form.html'
    permission_required = 'base.change_training'

    def form_valid(self, form):
        form.instance.editor_id = self.request.user.id
        return super(TrainingUpdate, self).form_valid(form)


class TrainingDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Training
    success_url = reverse_lazy('training_list')
    template_name = 'base/_confirm_delete.html'
    permission_required = 'base.delete_training'

    def get_context_data(self, **kwargs):
        ctx = super(TrainingDelete, self).get_context_data(**kwargs)
        ctx['object_primary_name'] = getattr(self.get_object(), 'subject')
        ctx['object_secondary_name'] = getattr(self.get_object(), 'date')
        ctx['object_class_name'] = force_text(self.model._meta.verbose_name)
        return ctx


class MessageList(ListView):
    model = Message
    template_name = 'base/message_list.html'


class MessageCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    success_url = reverse_lazy('message_list')
    form_class = MessageForm
    template_name = 'base/message_form.html'
    permission_required = 'base.add_message'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.editor_id = self.request.user.id
        form.instance.creation_date = timezone.now()
        return super(MessageCreate, self).form_valid(form)


class MessageUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    success_url = reverse_lazy('message_list')
    form_class = MessageForm
    template_name = 'base/message_form.html'
    permission_required = 'base.change_message'

    def form_valid(self, form):
        form.instance.editor_id = self.request.user.id
        return super(MessageUpdate, self).form_valid(form)


class MessageDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message_list')
    template_name = 'base/_confirm_delete.html'
    permission_required = 'base.delete_message'

    def get_context_data(self, **kwargs):
        ctx = super(MessageDelete, self).get_context_data(**kwargs)
        ctx['object_primary_name'] = getattr(self.get_object(), 'subject')
        ctx['object_secondary_name'] = getattr(self.get_object(), 'creation_date')
        ctx['object_class_name'] = force_text(self.model._meta.verbose_name)
        return ctx


class BPCarrierList(ListView):
    model = UserProfile
    template_name = 'base/bpcarrier_list.html'

    def get_queryset(self):
        queryset = super(BPCarrierList, self).get_queryset()
        return queryset.filter(breathing_protection_carrier=True)


class BPCarrierUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = UserProfile
    success_url = reverse_lazy('bpcarrier_list')
    form_class = BPCarrierForm
    template_name = 'base/bpcarrier_form.html'
    permission_required = 'base.change_breathingprotectioncarrier'

    def form_valid(self, form):
        form.instance.editor_id = self.request.user.id
        return super(BPCarrierUpdate, self).form_valid(form)


class UserImport(TemplateView):
    template_name = 'base/user_import.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        ctx = super(UserImport, self).get_context_data(**kwargs)
        importer = UserImporter()
        ctx['users'] = importer.get_users_from_csv_file()
        return ctx

    def post(self, request, *args, **kwargs):
        importer = UserImporter()
        users = importer.get_users_from_csv_file()
        importer.import_users(users, self.request.user)
        return HttpResponseRedirect(self.success_url)


class TrainingImport(TemplateView):
    template_name = 'base/training_import.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        ctx = super(TrainingImport, self).get_context_data(**kwargs)
        importer = TrainingImporter()
        ctx['trainings'] = importer.get_trainings_from_csv_file()
        return ctx

    def post(self, request, *args, **kwargs):
        importer = TrainingImporter()
        importer.import_trainings(self.request.user)
        return HttpResponseRedirect(self.success_url)


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
