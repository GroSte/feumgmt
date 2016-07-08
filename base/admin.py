from django.contrib import admin
from base.models import Vehicle, UserProfile, Message, Municipality, FireHouse


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_str', 'phone_number', 'mobile_phone_number', 'birth_date')
    search_fields = ['phone_number', 'mobile_phone_number', 'birth_date']

    def user_str(self, obj):
        return u'{0}, {1}'.format(obj.user.last_name, obj.user.first_name)


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


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(FireHouse, FireHouseAdmin)
