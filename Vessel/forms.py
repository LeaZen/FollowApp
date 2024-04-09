from django import forms 
from django.forms.models import inlineformset_factory
from .models import *


class VesselPortsAgentFormset(forms.ModelForm):
     
    LoadingPortFormset = inlineformset_factory(Vessel, LoadingPort, fields=('loading_port_name', 'anchor_loading_port', 'eta_loading_port', 'etb_loading_port', 'ata_loading_port', 'atb_loading_port', 'etd_loading_port', 'atd_loading_port'), extra = 2)
    DischargePortFormset = inlineformset_factory(Vessel, DischargePort, fields=('discharge_port_name', 'anchor_discharge_port', 'eta_discharge_port', 'etb_discharge_port', 'ata_discharge_port', 'atd_discharge_port'), extra = 2)
    VesselAgentFormset = inlineformset_factory(Vessel, VesselAgent, fields=('vessel_agent_name', 'vessel_agent_info'), extra = 2)
    class Meta:
        model = Vessel  
        fields = ['vessel_name', 'vessel_imo', 'vessel_information', 'vessel_schedule', 'vessel_rotation']

"""
class VesselForm(forms.Form):
    
    # campos de Vessel

    vessel_name = forms.CharField(label='Vessel Name', max_length=50, required=True)
    vessel_imo = forms.IntegerField(label='Vessel IMO', required=False)
    vessel_information = forms.CharField(label='Vessel Information', widget=forms.Textarea, required=False)
    vessel_schedule = forms.CharField(label='Vessel Schedule', widget=forms.Textarea, required=False)
    vessel_rotation = forms.CharField(label='Vessel Rotation', widget=forms.Textarea, required=False)
    
    # campos de LoadingPort

    loading_port_name = forms.CharField(label='Loading Port Name', required=False)
    anchor_loading_port = forms.DateField(label='Anchor pol', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    eta_loading_port = forms.DateField(label='ETA pol', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    etb_loading_port = forms.DateField(label='ETB pol', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    ata_loading_port = forms.DateField(label='ATA pol', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    atb_loading_port = forms.DateField(label='ATB pol', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    etd_loading_port = forms.DateField(label='ETD pol', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    atd_loading_port = forms.DateField(label='ATD pol', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    # campos de DischargePort

    discharge_port_name = forms.CharField(label='Discharge Port Name', required=False)
    anchor_discharge_port = forms.DateField(label='Anchor pod', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    eta_discharge_port = forms.DateField(label='ETA pod', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    etb_discharge_port = forms.DateField(label='ETB pod', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    ata_discharge_port = forms.DateField(label='ATA pod', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    atd_discharge_port = forms.DateField(label='ATD pod', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    # campos de VesselAgent
    vessel_agent_name= forms.CharField(label='Agent', required=False)
    vessel_agent_info = forms.CharField(label='Agent Information', widget=forms.Textarea, required=False)
"""

class PruebaFormulario(forms.Form):

    vessel_name = forms.CharField(required=True)
    vessel_imo = forms.IntegerField(required=False)