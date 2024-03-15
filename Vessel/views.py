from django.shortcuts import render
from .models import Vessel, LoadingPort, DischargePort, VesselAgent
from datetime import date, timedelta
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.list import ListView


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
           
          # Itera sobre las naves relacionadas y obtiene el nombre de cada una
          
          if i.eta_discharge_port is not None and today <= maybeUnloaded:    
                existingDates.append((i.eta_discharge_port, i.assigned_vessel_pod, i.discharge_port_name))

          else:
                # Si eta_discharge_port es None, agregar el buque con "n/a"
                existingDates.append(("N/A", i.assigned_vessel_pod, i.discharge_port_name))

    # Ordenar por fecha o considerar "n/a" al final
    sorted_existingDates = sorted(existingDates, key=lambda x: x[0] if isinstance(x[0], date) else date.max)
    
     
    return render(request, "expected_arrivals.html", {"expected_arrivals": sorted_existingDates })



def loading_port_detail (request):

    mv = Vessel.objects.all()
    mv_ports = []

    for vessel in mv:
        ports_of_vessel = vessel.loading_port.all()
        port_list = [port.loading_port_name for port in ports_of_vessel]
        mv_ports.append((vessel.vessel_name, port_list))
        
    print (mv_ports)
    print (type (mv_ports))

    return render(request, "loading_port_detail.html", {"loading_port_detail": mv_ports })

"""
    mv = Vessel.objects.all()
    mv_ports = LoadingPort.objects.filter(assigned_vessel_pol=21)
"""

"""
    if Vessel.loading_port.all:
     print (Vessel.loading_port.all)
     for loading_port in Vessel.loading_port.all:
         loading_port.loading_port_name 
    else:
          "No loading ports available."
""" 


class VesselList(ListView):
    model = Vessel 
    template_name = "vessel_list.html"
    context_object_name = "vessels"


    """
    def get_queryset(self):
        # Imprimir información para depuración
        for vessel in Vessel.objects.all():
            print(f"Vessel: {vessel.vessel_name}")
            for loading_port in vessel.loading_port.all():
                print(f"Loading Port: {loading_port}")

        return Vessel.objects.all()
    """
"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén la instancia del modelo
        vessel_instance = Vessel.objects.all()
        # Agrega la instancia al contexto con el nombre 'vessel'
        context['vessel'] = vessel_instance
        return context
"""    

class VesselDetail(DetailView):
    model = Vessel
    template_name = "vessel_detail.html"
    context_object_name = "vessel"

    def get(self, request, *args, **kwargs): 
       self.object = self.get_object()
       return self.ports_dates(request, *args, **kwargs)
        
    def ports_dates (self, request, *args, **kwargs):
        
     # Obtener el ID de la embarcación de la URL
     vessel_id = self.kwargs.get('pk')
     print("Vessel ID from URL:", vessel_id)
        
     # Filtrar los puertos de carga correspondientes a la embarcación
     loading_ports = LoadingPort.objects.filter(assigned_vessel_pol_id=vessel_id)
     print("Loading ports associated with vessel:", loading_ports)
        
     loading_date_list = []
     for port in loading_ports:
            loading_date_list.append({
                'Port_name': port.loading_port_name,
                'Anchor': port.anchor_loading_port,
                'ETA': port.eta_loading_port,
                'ETB': port.etb_loading_port,
                'ATA': port.ata_loading_port,
                'ATB': port.atb_loading_port,
                'ETD': port.etd_loading_port,
                'ATD': port.atd_loading_port,
            })
     print (type (loading_date_list))
     print("Date list for vessel {}: {}".format(vessel_id, loading_date_list))
        

     # Filtrar los puertos de descarga correspondientes a la embarcación
     discharge_ports = DischargePort.objects.filter(assigned_vessel_pod_id=vessel_id)
     print("Discharge ports associated with vessel:", discharge_ports)

     discharge_date_list = []
     for port in discharge_ports:
            discharge_date_list.append({
                'Port_name': port.discharge_port_name,
                'Anchor': port.anchor_discharge_port,
                'ETA': port.eta_discharge_port,
                'ETB': port.etb_discharge_port,
                'ATA': port.ata_discharge_port,
                'ATD': port.atd_discharge_port,
            })
     print (type (discharge_date_list))
     print("Date list for vessel {}: {}".format(vessel_id, discharge_date_list))
        
     agent_vessel = VesselAgent.objects.filter(assigned_vessel_id=vessel_id)
     print("Loading ports associated with vessel:", agent_vessel)
     
     agent_vessel_list = []
     for agent in agent_vessel:
            agent_vessel_list.append({
                'Agent_name': agent.vessel_agent_name,
                'Agent_info': agent.vessel_agent_info,
            })

     context = {
            "loading_date_list": loading_date_list,
            "discharge_date_list": discharge_date_list,
            "vessel": self.object,
            "assigned_agent": agent_vessel_list,
            }
    

     return render(request, "vessel_detail.html", context)
    
        


class VesselCreate(CreateView):
    model = Vessel
    template_name = "vessel_create.html"
    fields = ["vessel_name","vessel_imo"]
    success_url = ('vessel/')

class VesselUpdate(UpdateView):
    model = Vessel
    template_name = "vessel_update.html"
    fields = ["__all__"]
    success_url = ('vessel/')

class VesselDelete(DeleteView):
    model = Vessel
    tate_name = "vessel_delete.html"
    success_url = ('vessel/')

 
