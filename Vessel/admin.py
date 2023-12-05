from django.contrib import admin
from.models import Vessel

class VesselAdmin (admin.ModelAdmin):
    search_fields = ['vessel_name', 'vessel_imo']

# Register your models here.
admin.site.register(Vessel, VesselAdmin)