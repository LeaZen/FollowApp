from django.db import models

# Create your models here.

class LoadingPort(models.Model):

    loading_port_name = models.CharField(max_length=50, blank=True, null=True)
    anchor_loading_port = models.DateField(blank=True, null=True)
    eta_loading_port = models.DateField(blank=True, null=True)
    etb_loading_port = models.DateField(blank=True, null=True)
    ata_loading_port = models.DateField(blank=True, null=True)
    atb_loading_port = models.DateField(blank=True, null=True)
    etd_loading_port = models.DateField(blank=True, null=True)
    atd_loading_port = models.DateField(blank=True, null=True)
    assigned_vessel_pol = models.ForeignKey('Vessel', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return  f"{self.loading_port_name}"
class DischargePort(models.Model):

    discharge_port_name = models.CharField(max_length=50, blank=True, null=True)
    anchor_discharge_port = models.DateField(blank=True, null=True)
    eta_discharge_port = models.DateField(blank=True, null=True) 
    etb_discharge_port = models.DateField(blank=True, null=True)  
    ata_discharge_port = models.DateField(blank=True, null=True)
    atd_discharge_port = models.DateField(blank=True, null=True)
    assigned_vessel_pod = models.ForeignKey('Vessel', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.discharge_port_name}, {self.assigned_vessel_pod}"
    

class VesselAgent(models.Model):

    vessel_agent_name = models.CharField(max_length=50, blank=True, null=True)
    vessel_agent_info = models.TextField(blank=True, null=True)
    assigned_vessel = models.ForeignKey('Vessel', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vessel_agent_name}"
    
class Vessel(models.Model):

    vessel_name = models.CharField(max_length=50)
    vessel_imo = models.IntegerField(blank=True, null=True)
    vessel_information = models.TextField(blank=True, null=True)
    vessel_schedule = models.TextField(blank=True, null=True)
    vessel_rotation = models.TextField(blank=True, null=True)
    loading_port = models.ManyToManyField(LoadingPort, blank=True)
    status_loading = models.BooleanField(blank=True, null=True)
    discharge_port = models.ManyToManyField(DischargePort, blank=True)
    status_loaded = models.BooleanField(blank=True, null=True)
    status_arrived = models.BooleanField(blank=True, null=True)
    all_docs_received = models.BooleanField(blank=True, null=True)
    all_dhl_received = models.BooleanField(blank=True, null=True)
    status_complete = models.BooleanField(blank=True, null=True)
    assigned_agent = models.ManyToManyField(VesselAgent, blank=True)
    transit_time = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.vessel_name
    
    """
    def obtener_atributo(self, vessel_name):
        return getattr(self, vessel_name, None)
    """