from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from base.models import Mission

admin.site.register(Mission, LeafletGeoAdmin)
