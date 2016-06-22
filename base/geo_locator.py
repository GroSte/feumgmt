# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib
import urllib2
from django.utils.translation import ugettext_lazy as _
from geopy import Nominatim

from geopy.exc import GeocoderTimedOut


class GeoLocator(object):
    base_address_url = 'http://www.mapquestapi.com/geocoding/v1/address'
    base_route_url = 'http://www.mapquestapi.com/directions/v2/route'
    home_address = 'Am Quellenberg A 1a, Dürrröhrsdorf-Dittersbach'

    def get_location_coordinates(self, key, address):
        # use mapquest
        address = self._escape_address(address)
        quoted_address = urllib.quote(address)
        url = self.base_address_url + '?key={0}&location={1}'.format(key, quoted_address)
        response = urllib2.urlopen(url)
        result = json.load(response)
        try:
            loc = result['results'][0]['locations'][0]
            return {
                'lat': loc['latLng']['lat'],
                'long': loc['latLng']['lng'],
            }
        except Exception:
            pass

        # if no location was found use nominatim
        geolocator = Nominatim(
            format_string="%s, Landkreis Sächsische Schweiz-Osterzgebirge, Sachsen, 01833, Deutschland")
        try:
            locations = geolocator.geocode(address, False)
        except GeocoderTimedOut:
            locations = None

        if locations:
            location = locations[0]
            return {
                'lat': float(location.latitude),
                'long': float(location.longitude),
                # 'address': location.address,
                # 'raw': location.raw,
            }
        return {}

    def get_route(self, key, to_address, from_address=None):
        home = from_address if from_address else self.home_address
        home = self._escape_address(home)
        to_address = self._escape_address(to_address)
        quoted_address = urllib.quote(to_address)
        quoted_home = urllib.quote(home)

        url_route = self.base_route_url + '?key={0}&from={1}&to={2}&locale=de_DE&unit=k'.format(
            key, quoted_home, quoted_address)
        response = urllib2.urlopen(url_route)
        result = json.load(response)

        try:
            route = result['route']
            dist = route['distance']
            minutes, seconds = divmod(route['time'], 60)
            return {
                'distance': _('{0} km').format(round(dist, 3)),
                'time': _('{0} min {1} s').format(minutes, seconds),
            }
        except Exception:
            pass
        return {}

    def _escape_address(self, address):
        address = address.replace('ö', 'oe')
        address = address.replace('ä', 'ae')
        address = address.replace('ü', 'ue')
        address = address.replace('ß', 'ss')
        return address
