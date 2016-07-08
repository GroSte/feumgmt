from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from event.models import Training, Mission, BreathingProtectionTraining


class BreathingProtectionTrainingAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'organizer')
    search_fields = ['date', 'location']


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('date', 'subject', 'note')
    search_fields = ['date', 'subject', 'note']


class MissionAdmin(LeafletGeoAdmin):
    list_display = ('alarm_time', 'keyword_str', 'location', 'street')
    search_fields = ['alarm_time', 'keyword', 'volume', 'concerned', 'location', 'street']

    def keyword_str(self, obj):
        return u'{0}-{1}-{2}'.format(obj.keyword, obj.volume, obj.concerned)


admin.site.register(Mission, MissionAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(BreathingProtectionTraining, BreathingProtectionTrainingAdmin)
