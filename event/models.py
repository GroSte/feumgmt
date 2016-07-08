# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from djgeojson.fields import PointField

from base.models import UserProfile, Vehicle


class Training(models.Model):
    date = models.DateTimeField(max_length=100, verbose_name=_('Date'))
    subject = models.CharField(max_length=200, verbose_name=_('Subject'))
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Note'))
    responsibles = models.ManyToManyField(UserProfile, blank=True,
                                          related_name='training_responsibles',
                                          verbose_name=_('Responsibles'))

    editor = models.ForeignKey(UserProfile, null=True, blank=True, related_name='training_editor',
                               verbose_name=_('Editor'))
    creation_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation date'))
    last_update = models.DateTimeField(null=True, auto_now=True, verbose_name=_('Last update'))

    class Meta:
        verbose_name = _('Training')
        verbose_name_plural = _('Trainings')
        ordering = ('-date',)

        permissions = (
            ("view_training", _('Can view trainings')),
        )

    def __unicode__(self):
        return '{0} - {1}'.format(self.date, self.subject)


class BreathingProtectionTraining(models.Model):
    date = models.DateTimeField(max_length=100, verbose_name=_('Date'))
    location = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Location'))
    organizer = models.ForeignKey(UserProfile, verbose_name=_('Organizer'),
                                  related_name='bpt_organizer')
    participants = models.ManyToManyField(UserProfile, blank=True,
                                          related_name='bpt_participants',
                                          verbose_name=_('Participants'))

    editor = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name=_('Editor'))
    creation_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation date'))
    last_update = models.DateTimeField(null=True, auto_now=True, verbose_name=_('Last update'))

    class Meta:
        verbose_name = _('Breathing Protection Training')
        verbose_name_plural = _('Breathing Protection Trainings')
        ordering = ('-date',)

        permissions = (
            ("view_breathingprotectiontraining", _('Can view breathing protection trainings')),
        )

    def __unicode__(self):
        return '{0} - {1}'.format(self.date, self.location)


class Mission(models.Model):
    number = models.CharField(blank=True, null=True, max_length=20,
                              verbose_name=_('Number'))  # Einsatz-Nummer
    alarm_time = models.DateTimeField(verbose_name=_('Alarm Time'))  # Alarmierungszeit
    keyword = models.CharField(max_length=100, verbose_name=_('Keyword'),
                               db_index=True)  # Stichwort
    description = models.TextField(blank=True, null=True,
                                   verbose_name=_('Description'))  # Beschreibung
    volume = models.CharField(blank=True, null=True, max_length=100,
                              verbose_name=_('Volume'))  # Umfang, Groesse
    concerned = models.CharField(blank=True, null=True, max_length=20,
                                 verbose_name=_('Concerned'))  # Betroffene
    name = models.CharField(blank=True, null=True, max_length=200, verbose_name=_('Name'))  # Name
    street = models.CharField(max_length=200, verbose_name=_('Street'))  # Strasse
    location = models.CharField(max_length=200, verbose_name=_('Location'))  # Ort
    coordinates = PointField(blank=True, null=True, verbose_name=_('Coordinates'))  # Koordinaten
    signal = models.BooleanField(default=True, verbose_name=_('Signal'))  # Sondersignal
    vehicles = models.ManyToManyField(Vehicle, blank=True, verbose_name=_('Vehicles'))  # Fahrzeuge
    firefighters = models.ManyToManyField(UserProfile, blank=True,
                                          related_name='mission_firefighters',
                                          verbose_name=_('Firefighters'))  # Einsatzkraefte

    editor = models.ForeignKey(UserProfile, null=True, blank=True, related_name='mission_editor',
                               verbose_name=_('Editor'))
    creation_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation date'))
    last_update = models.DateTimeField(null=True, auto_now=True, verbose_name=_('Last update'))

    class Meta:
        verbose_name = _('Mission')
        verbose_name_plural = _('Missions')
        ordering = ('-alarm_time',)

        permissions = (
            ("view_mission", _('Can view missions')),
        )

    def __unicode__(self):
        return '{0}-{1}-{2} {3}'.format(self.keyword, self.volume, self.concerned, self.location)
