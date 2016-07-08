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

from base.forms import MessageForm, UserPasswordChangeForm
from base.importer import UserImporter
from base.models import Message, UserProfile
from event.models import Training, BreathingProtectionTraining
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
        except AttributeError:
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
        except AttributeError:
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
