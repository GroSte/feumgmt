from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djgeojson.fields import PointField


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
    online = models.BooleanField(default=False, verbose_name=_('Online'))
    online_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Online date'))
    online_ip = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Online IP'))

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)


class Vehicle(models.Model):
    call_sign = models.CharField(max_length=100, verbose_name=_('Call Sign'))# Kenner
    crew = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Crew'))# Besatzung
    badge = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Badge'))# Kennzeichen

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')

    def __str__(self):
        return self.call_sign


class Training(models.Model):
    date = models.DateTimeField(max_length=100, verbose_name=_('Date'))
    subject = models.CharField(max_length=200, verbose_name=_('Subject'))
    hint = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Hint'))
    firefighters = models.ManyToManyField(UserProfile, verbose_name='Firefighters')

    class Meta:
        verbose_name = _('Training')
        verbose_name_plural = _('Trainings')

    def __str__(self):
        return '{0} - {1}'.format(self.date, self.subject)


class BreathingProtectionTraining(models.Model):
    date = models.DateTimeField(max_length=100, verbose_name=_('Date'))
    location = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Location'))
    organizer = models.ForeignKey(UserProfile, verbose_name=_('Organizer'),
                                  related_name='bpt_organizer')
    firefighters = models.ManyToManyField(UserProfile, related_name='bpt_firefighters',
                                          verbose_name=_('Firefighters'))

    class Meta:
        verbose_name = _('Breathing Protection Training')
        verbose_name_plural = _('Breathing Protection Trainings')

    def __str__(self):
        return '{0} - {1}'.format(self.date, self.location)


class Mission(models.Model):
    number = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Number'))  # Einsatz-Nummer
    alarm_time = models.DateTimeField(verbose_name=_('Alarm Time'))  # Alarmierungszeit
    keyword = models.CharField(max_length=100, verbose_name=_('Keyword'), db_index=True)  # Stichwort
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))  # Beschreibung
    volume = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('Volume'))  # Umfang, Groesse
    concerned = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Concerned'))  # Betroffene
    name = models.CharField(blank=True, null=True, max_length=200, verbose_name=_('Name'))  # Name
    street = models.CharField(max_length=200, verbose_name=_('Street'))  # Strasse
    location = models.CharField(max_length=200, verbose_name=_('Location'))  # Ort
    coordinates = PointField(blank=True, null=True, verbose_name=_('Coordinates'))  # Koordinaten
    signal = models.BooleanField(default=True, verbose_name=_('Signal'))  # Sondersignal
    vehicles = models.ManyToManyField(Vehicle)  # Fahrzeuge
    firefighters = models.ManyToManyField(UserProfile)  # Einsatzkraefte

    class Meta:
        verbose_name = _('Mission')
        verbose_name_plural = _('Missions')

    def __str__(self):
        return '{0} / {1} - {2}'.format(self.number, self.keyword, self.location)
