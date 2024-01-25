from django.contrib import admin
from.models import Vessel, LoadingPort, DischargePort, VesselAgent


class LoadingPortInline(admin.TabularInline):  # O también puedes usar StackedInline
    model = LoadingPort
    extra = 1  # Número de formularios en blanco a mostrar
class DischargePortInline(admin.TabularInline):  # O también puedes usar StackedInline
    model = DischargePort
    extra = 1  # Número de formularios en blanco a mostrar
class VesselAgentInline(admin.StackedInline):  # O también puedes usar StackedInline
    model = VesselAgent
    extra = 1  # Número de formularios en blanco a mostrar
class VesselAdmin (admin.ModelAdmin):
    search_fields = ['vessel_name', 'vessel_imo']
    inlines = [LoadingPortInline, DischargePortInline, VesselAgentInline]
    exclude = ('loading_port', 'discharge_port', 'assigned_agent')


# Register your models here.
admin.site.register(Vessel, VesselAdmin)
admin.site.register(LoadingPort)
admin.site.register(DischargePort)
admin.site.register(VesselAgent)
