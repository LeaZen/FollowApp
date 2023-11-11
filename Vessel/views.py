from django.shortcuts import render
from .models import Vessel
from datetime import date

# Create your views here.
def inicio (request):
    return render(request, "inicio.html")

def vessels_to_load (request):
    
    vesselsList = Vessel.objects.all()
    availableDates = []

    if vesselsList.exists():

        for i in vesselsList:

            if i.atd_loading_port:
                pass
            elif i.ata_loading_port: 
                availableDates.append((i.ata_loading_port, i.vessel_name, i.loading_port))
            elif i.atb_loading_port:
                availableDates.append((i.atb_loading_port, i.vessel_name, i.loading_port))
            elif i.etb_loading_port:
                availableDates.append((i.etb_loading_port, i.vessel_name, i.loading_port))
            elif i.eta_loading_port:
                availableDates.append((i.eta_loading_port, i.vessel_name, i.loading_port))
            elif i.anchor_loading_port:
                availableDates.append((i.anchor_loading_port, i.vessel_name, i.loading_port))
        else:
            pass
            
        
        sorted_availableDates = sorted(availableDates)
        print (sorted_availableDates)
        return render(request, "vessels_to_load.html", {"vessels_to_load":sorted_availableDates})

        

def expected_arrivals (request):

    vesselsList = Vessel.objects.all()
    existingDates = []

    if vesselsList.exists():

        for i in vesselsList:

            if i.eta_discharge_port: 
                existingDates.append((i.eta_discharge_port, i.vessel_name, i.discharge_port))
        else:
            pass
            
        sorted_existingDates = sorted(existingDates)
        print (sorted_existingDates)

    return render(request, "expected_arrivals.html", {"expected_arrivals": sorted_existingDates })

