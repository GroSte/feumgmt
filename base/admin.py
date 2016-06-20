from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from base.models import Mission, Vehicle

admin.site.register(Mission, LeafletGeoAdmin)
admin.site.register(Vehicle)
