from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from base.models import Mission, Vehicle, UserProfile, BreathingProtectionTraining, Training, \
    Message, Municipality, FireHouse


class BreathingProtectionTrainingAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'organizer')
    search_fields = ['date', 'location']


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('date', 'subject', 'note')
    search_fields = ['date', 'subject', 'note']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_str', 'phone_number', 'mobile_phone_number', 'birth_date')
    search_fields = ['phone_number', 'mobile_phone_number', 'birth_date']

    def user_str(self, obj):
        return u'{0}, {1}'.format(obj.user.last_name, obj.user.first_name)


class MissionAdmin(LeafletGeoAdmin):
    list_display = ('alarm_time', 'keyword_str', 'location', 'street')
    search_fields = ['alarm_time', 'keyword', 'volume', 'concerned', 'location', 'street']

    def keyword_str(self, obj):
        return u'{0}-{1}-{2}'.format(obj.keyword, obj.volume, obj.concerned)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('call_sign', 'fire_house')
    search_fields = ['call_sign', 'fire_house']


class FireHouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'street', 'chief')
    search_fields = ['name', 'location', 'street', 'chief']


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'street', 'chief')
    search_fields = ['name', 'location', 'street', 'chief']


class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'author', 'expiration_date')
    search_fields = ['subject', 'author', 'expiration_date']


admin.site.register(Mission, MissionAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(BreathingProtectionTraining, BreathingProtectionTrainingAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(FireHouse, FireHouseAdmin)
