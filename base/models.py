# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from djgeojson.fields import PointField
import operator


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    grade = models.CharField(max_length=20, blank=True, null=True,
                             verbose_name=_('Grade'))
    phone_number = models.CharField(max_length=25, blank=True, null=True,
                                    verbose_name=_('Phone Number'))
    mobile_phone_number = models.CharField(max_length=25, blank=True, null=True,
                                           verbose_name=_('Mobile Phone Number'))
    birth_date = models.DateField(max_length=45, blank=True, null=True,
                                  verbose_name=_('Birth Date'))
    admittance_date = models.DateField(blank=True, null=True,
                                       verbose_name=_('Admittance Date'))  # Eintrittsdatum
    breathing_protection_carrier = models.BooleanField(
        default=False,
        verbose_name=_('Breathing Protection Carrier'))  # ASG-Traeger
    next_medical_examination_date = models.DateField(
        blank=True, null=True, verbose_name=_('Next Medical Examination Date'))  # naechste G26
    next_breathing_protection_training_date = models.DateField(
        blank=True, null=True,
        verbose_name=_('Next Breathing Protection Training Date'))  # naechster ASUE-Termin
    online = models.BooleanField(default=False, verbose_name=_('Online'))
    online_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Online date'))
    online_ip = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Online IP'))

    creation_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation date'))
    last_update = models.DateTimeField(null=True, auto_now=True, verbose_name=_('Last update'))

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('user__last_name',)

        permissions = (
            ("view_breathingprotectioncarrier", _('Can view breathing protection carriers')),
            ("change_breathingprotectioncarrier", _('Can change breathing protection carrier')),
        )

    def __unicode__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)

    @staticmethod
    def get_next_birthdays(days):
        now = datetime.now()
        then = now + timedelta(days)

        monthdays = [(now.month, now.day)]
        while now <= then:
            monthdays.append((now.month, now.day))
            now += timedelta(days=1)

        monthdays = (dict(zip(("birth_date__month", "birth_date__day"), t))
                     for t in monthdays)
        query = reduce(operator.or_, (Q(**d) for d in monthdays))
        users = UserProfile.objects.filter(query).order_by('birth_date')
        listing = []
        for user in users:
            age = now.year - user.birth_date.year - (
                (now.month, now.day) < (user.birth_date.month, user.birth_date.day))
            if now.month == 12 and user.birth_date.strftime('%m') == '1':
                # HACK to sort january after last december birthdays
                index = '13' + user.birth_date.strftime('%d')
            else:
                index = user.birth_date.strftime('%m%d')
            listing.append(
                {
                    'index': index,
                    'name': str(user),
                    'day': user.birth_date,
                    'age': age,
                }
            )
        listing.sort(key=lambda s: s['index'])
        return listing


class Municipality(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    chief = models.CharField(max_length=200, null=True, blank=True,
                             verbose_name=_('Chief'))  # Gemeindewehrleiter
    street = models.CharField(max_length=200, null=True, blank=True,
                              verbose_name=_('Street'))  # Strasse
    location = models.CharField(max_length=200, null=True, blank=True,
                                verbose_name=_('Location'))  # Ort
    phone_number = models.CharField(max_length=25, blank=True, null=True,
                                    verbose_name=_('Phone Number'))

    editor = models.ForeignKey(UserProfile, null=True, blank=True,
                               related_name='municipality_editor', verbose_name=_('Editor'))
    creation_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation date'))
    last_update = models.DateTimeField(null=True, auto_now=True, verbose_name=_('Last update'))

    class Meta:
        verbose_name = _('Municipality')
        verbose_name_plural = _('Municipalities')
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class FireHouse(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    chief = models.CharField(max_length=200, null=True, blank=True,
                             verbose_name=_('Chief'))  # Wehrleiter
    street = models.CharField(max_length=200, null=True, blank=True,
                              verbose_name=_('Street'))  # Strasse
    location = models.CharField(max_length=200, null=True, blank=True,
                                verbose_name=_('Location'))  # Ort
    phone_number = models.CharField(max_length=25, blank=True, null=True,
                                    verbose_name=_('Phone Number'))
    municipality = models.ForeignKey(Municipality, null=True, blank=True,
                                     verbose_name=_('Municipality'))

    editor = models.ForeignKey(UserProfile, null=True, blank=True,
                               related_name='fire_house_editor', verbose_name=_('Editor'))
    creation_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation date'))
    last_update = models.DateTimeField(null=True, auto_now=True, verbose_name=_('Last update'))

    class Meta:
        verbose_name = _('Fire House')
        verbose_name_plural = _('Fire Houses')
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Vehicle(models.Model):
    call_sign = models.CharField(max_length=100, verbose_name=_('Call Sign'))  # Kenner
    crew = models.CharField(blank=True, null=True, max_length=20,
                            verbose_name=_('Crew'))  # Besatzung
    number_plate = models.CharField(blank=True, null=True, max_length=20,
                                    verbose_name=_('Number Plate'))  # Kennzeichen
    fire_house = models.ForeignKey(FireHouse, null=True, blank=True, verbose_name=_('Fire House'))

    editor = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name=_('Editor'))
    creation_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation date'))
    last_update = models.DateTimeField(null=True, auto_now=True, verbose_name=_('Last update'))

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')
        ordering = ('call_sign',)

    def __unicode__(self):
        return self.call_sign


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


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name=_('Subject'))
    text = models.TextField(verbose_name=_('Text'))
    expiration_date = models.DateField(null=True, blank=True, verbose_name=_('Expiration Date'))
    author = models.ForeignKey(UserProfile, related_name='message_author',
                               verbose_name=_('Author'))

    editor = models.ForeignKey(UserProfile, null=True, blank=True, related_name='message_editor',
                               verbose_name=_('Editor'))
    creation_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Creation date'))
    last_update = models.DateTimeField(null=True, auto_now=True, verbose_name=_('Last update'))

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('-creation_date',)

        permissions = (
            ("view_message", _('Can view messages')),
        )

    def __unicode__(self):
        return '{0} ({1})'.format(self.subject, self.author)
