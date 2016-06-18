from django.db import models
from django.utils.translation import ugettext_lazy as _
from djgeojson.fields import PointField


class Vehicle(models.Model):
    call_sign = models.CharField(max_length=100, verbose_name=_('Call Sign'))# Kenner
    crew = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Crew'))# Besatzung
    badge = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Badge'))# Kennzeichen

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')

    def __str__(self):
        return self.call_sign


class Mission(models.Model):
    number = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Number')) # Einsatz-Nummer
    alarm_time = models.DateTimeField(verbose_name=_('Alarm Time')) # Alarmierungszeit
    keyword = models.CharField(max_length=100, verbose_name=_('Keyword'), db_index=True) # Stichwort
    description = models.TextField(blank=True, null=True, verbose_name=_('Description')) # Beschreibung
    volume = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('Volume')) # Umfang, Groesse
    concerned = models.CharField(blank=True, null=True, max_length=20, verbose_name=_('Concerned')) # Betroffene
    name = models.CharField(blank=True, null=True, max_length=200, verbose_name=_('Name')) # Name
    street = models.CharField(max_length=200, verbose_name=_('Street')) # Strasse
    location = models.CharField(max_length=200, verbose_name=_('Location')) # Ort
    coordinates = PointField(blank=True, null=True, verbose_name=_('Coordinates')) # Koordinaten
    signal = models.BooleanField(default=True, verbose_name=_('Signal')) # Sondersignal
    vehicles = models.ManyToManyField(Vehicle) # Fahrzeuge

    class Meta:
        verbose_name = _('Mission')
        verbose_name_plural = _('Missions')

    def __str__(self):
        return '{0} / {1} - {2}'.format(self.number, self.keyword, self.location)
