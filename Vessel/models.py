from django.db import models

# Create your models here.

class Vessel(models.Model):

    vessel_name = models.CharField(max_length=50)
    vessel_imo = models.IntegerField(blank=True, null=True)
    vessel_information = models.TextField(blank=True, null=True)
    vessel_schedule = models.TextField(blank=True, null=True)
    vessel_rotation = models.TextField(blank=True, null=True)
    transit_time = models.IntegerField(blank=True, null=True)
    loading_port = models.CharField(max_length=50, blank=True, null=True)
    anchor_loading_port = models.DateField(blank=True, null=True)
    eta_loading_port = models.DateField(blank=True, null=True)
    etb_loading_port = models.DateField(blank=True, null=True)
    ata_loading_port = models.DateField(blank=True, null=True)
    atb_loading_port = models.DateField(blank=True, null=True)
    etd_loading_port = models.DateField(blank=True, null=True)
    atd_loading_port = models.DateField(blank=True, null=True)
    discharge_port = models.CharField(max_length=50, blank=True, null=True)
    eta_discharge_port = models.DateField(blank=True, null=True)    

    def __str__(self):
        return self.vessel_name