from django.shortcuts import render
from .models import Vessel, LoadingPort, DischargePort, VesselAgent
from datetime import date, timedelta

# Create your views here.
def inicio (request):
    return render(request, "inicio.html")

def vessels_to_load (request):
    
    vesselsList = LoadingPort.objects.all()
    availableDates = []

    today = date.today()

    if vesselsList.exists():

        for i in vesselsList:

            if i.atd_loading_port:
                pass
            elif i.ata_loading_port: 
                availableDates.append((i.ata_loading_port, i.assigned_vessel_pol, i.loading_port_name))
            elif i.atb_loading_port:
                availableDates.append((i.atb_loading_port, i.assigned_vessel_pol, i.loading_port_name))
            elif i.etb_loading_port:
                availableDates.append((i.etb_loading_port, i.assigned_vessel_pol, i.loading_port_name))
            elif i.eta_loading_port:
                availableDates.append((i.eta_loading_port, i.assigned_vessel_pol, i.loading_port_name))
            elif i.anchor_loading_port:
                availableDates.append((i.anchor_loading_port, i.assigned_vessel_pol, i.loading_port_name))
            else:
                availableDates.append(("N/A", i.assigned_vessel_pol, i.loading_port_name))
                
            # Filtrar y ordenar las fechas          # Si no hay fecha, establecer "N/A" con una fecha máxima
            availableDates = sorted(availableDates, key=lambda x: x[0] if isinstance(x[0], date) else date.max)
                
            # Filtrar para mostrar fechas válidas dentro de los próximos 7 días, incluyendo las fechas "N/A" en el resultado final
            filteredDates = [
            (date_loading_port, vessel_name, loading_port)
            for date_loading_port, vessel_name, loading_port in availableDates   
             if (date_loading_port == "N/A") or (isinstance (date_loading_port, date) and (date_loading_port + timedelta(days=7)) >= today)
            ]
            
            
    return render(request, "vessels_to_load.html", {"vessels_to_load":filteredDates})


def expected_arrivals (request):

    vesselsList = DischargePort.objects.all()
    existingDates = []

    today = date.today()
    #print (type(maybeLoaded), "esto es la impresión")
    #print (type(Vessel.eta_discharge_port), "esto es eta dicharge")
    if vesselsList.exists():
          
      for i in vesselsList:
          
          if i.eta_discharge_port is not None:
           maybeUnloaded = i.eta_discharge_port + timedelta(days=7)
           #vessels = i.assigned_vessel_pod
          # Itera sobre las naves relacionadas y obtiene el nombre de cada una
          #for thevessel in vessels:
                #name_of_vessel = thevessel
          if i.eta_discharge_port is not None and today <= maybeUnloaded:    
                existingDates.append((i.eta_discharge_port, i.assigned_vessel_pod, i.discharge_port_name))

          else:
                # Si eta_discharge_port es None, agregar el buque con "n/a"
                existingDates.append(("N/A", i.assigned_vessel_pod, i.discharge_port_name))

    # Ordenar por fecha o considerar "n/a" al final
    sorted_existingDates = sorted(existingDates, key=lambda x: x[0] if isinstance(x[0], date) else date.max)
    #sorted_existingDates = sorted(existingDates, key=lambda x: x[0] if x[0] is not None else date.max)  
    #sorted_existingDates = sorted(existingDates)
     
    return render(request, "expected_arrivals.html", {"expected_arrivals": sorted_existingDates })

