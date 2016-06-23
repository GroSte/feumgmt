from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from base.models import Mission, Vehicle, UserProfile, BreathingProtectionTraining, Training, \
    Message

admin.site.register(Mission, LeafletGeoAdmin)
admin.site.register(Vehicle)
admin.site.register(UserProfile)
admin.site.register(Training)
admin.site.register(BreathingProtectionTraining)
admin.site.register(Message)
