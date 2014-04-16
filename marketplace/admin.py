from django.contrib import admin

from models import CarAd, MotorCycleAd


class VehicleAdAdmin(admin.ModelAdmin):
    pass


class MotorCycleAdAdmin(admin.ModelAdmin):
    pass

admin.site.register(CarAd, VehicleAdAdmin)
admin.site.register(MotorCycleAd, MotorCycleAdAdmin)
