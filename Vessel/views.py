from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Vessel, LoadingPort, DischargePort, VesselAgent
from datetime import date, timedelta
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.list import ListView
from .forms import VesselPortsAgentFormset, PruebaFormulario
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse

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


"""
# UNA FUNCIÓN QUE NO SE UTILIZA POR EL MOMENTO.

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

class VesselList(ListView):
    model = Vessel 
    template_name = "vessel_list.html"
    context_object_name = "vessels"
    #ordering = "-date.created"

def search_vessel(request):
        
    print ('method', request.method)
    print ('get', request.GET)
    
    if request.GET:
        vessel_name = request.GET.get("vessel_name", None)  # Obtener el nombre del buque de la solicitud GET
        vessel_imo = request.GET.get("vessel_imo", None) # Obtener el imo del buque de la solicitud GET
        
        if vessel_name:
            try:
                # Buscar el buque en la base de datos por su nombre.
                vessel = Vessel.objects.get(vessel_name=vessel_name)
                print("Vessel ID:", vessel.id)
                print("Vessel name", vessel.vessel_name)
                
                # Renderiza la plantilla Detail View con el resultado de la búsqueda.
                url = reverse('VesselDetail', kwargs={'pk': vessel.id}) + '?mensaje=Vessel Finded'
                return redirect (url)
            
                # Este era el return anterior:
                # return render(request, "search_vessel.html", {'vessel': vessel})    
            except Vessel.DoesNotExist:
                # Si el buque no se encuentra, devuelve un mensaje.
                return render(request, "search_vessel.html", { "message" : "Vessel cannot be found"})

        elif vessel_imo:
            try:
                vessel_imo = Vessel.objects.get(vessel_imo=vessel_imo)
                print ("Vessel IMO", vessel_imo)

                # Renderiza la plantilla Detail View con el resultado de la búsqueda.
                url = reverse('VesselDetail', kwargs={'pk': vessel_imo.id}) + '?mensaje=Vessel Finded'
                return redirect (url)

                # Este era el return anterior: 
                # return render (request, "search_vessel.html", {"vessel": vessel_imo})
            

            except Vessel.DoesNotExist:
                # Si el buque no se encuentra, devuelve un mensaje.
                return render(request, "search_vessel.html", { "message" : "Vessel cannot be found"})
            
    # Si no hay parámetros GET o el parámetro 'vessel_name' no está presente, renderiza la página de resultados vacía.
    return render(request, "search_vessel.html")

 
    
    
    

class VesselDetail(DetailView):
    model = Vessel
    template_name = "vessel_detail.html"
    context_object_name = "vessel"

    def get(self, request, *args, **kwargs): 
       self.object = self.get_object() # Obtiene el objeto del modelo `Vessel` basado en el `pk` pasado en la URL
       return self.ports_dates(request, *args, **kwargs) # Llama al método `ports_dates` y retorna su resultado
        
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
    #fields = ["vessel_name","vessel_imo"]
    #fields = '__all__' 
    form_class = VesselPortsAgentFormset
    success_url = '/vessel/vessels-list/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['loading_port_formset'] = self.form_class.LoadingPortFormset(self.request.POST, instance=self.object)
            data['discharge_port_formset'] = self.form_class.DischargePortFormset(self.request.POST, instance=self.object)
            data['vessel_agent_formset'] = self.form_class.VesselAgentFormset(self.request.POST, instance=self.object)
        else:
            data['loading_port_formset'] = self.form_class.LoadingPortFormset(instance=self.object)
            data['discharge_port_formset'] = self.form_class.DischargePortFormset(instance=self.object)
            data['vessel_agent_formset'] = self.form_class.VesselAgentFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        loading_port_formset = context['loading_port_formset']
        discharge_port_formset = context['discharge_port_formset']
        vessel_agent_formset = context['vessel_agent_formset']
        if loading_port_formset.is_valid() and discharge_port_formset.is_valid() and vessel_agent_formset.is_valid():
            self.object = form.save()
            loading_port_formset.instance = self.object
            loading_port_formset.save()
            discharge_port_formset.instance = self.object
            discharge_port_formset.save()
            vessel_agent_formset.instance = self.object
            vessel_agent_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

"""
    OTRA FORMA DE VESSEL CREATE
    def form_valid(self, form):
        # Guardar datos de Vessel
        vessel_name = form.cleaned_data['vessel_name']
        vessel_imo = form.cleaned_data['vessel_imo']
        vessel_information = form.cleaned_data['vessel_information']
        vessel_schedule = form.cleaned_data['vessel_schedule']
        vessel_rotation = form.cleaned_data['vessel_rotation']
        
        vessel = Vessel.objects.create(
            vessel_name=vessel_name,
            vessel_imo=vessel_imo,
            vessel_information=vessel_information,
            vessel_schedule=vessel_schedule,
            vessel_rotation=vessel_rotation
        )
        
        # Guardar datos de LoadingPort
        loading_port_name = form.cleaned_data['loading_port_name']
        anchor_loading_port = form.cleaned_data['anchor_loading_port']
        eta_loading_port = form.cleaned_data['eta_loading_port']
        etb_loading_port = form.cleaned_data['etb_loading_port']
        ata_loading_port = form.cleaned_data['ata_loading_port']
        atb_loading_port = form.cleaned_data['atb_loading_port']
        etd_loading_port = form.cleaned_data['etd_loading_port']
        atd_loading_port = form.cleaned_data['atd_loading_port']

        # Crea una instancia de LoadingPort y la asocia con el Vessel
        if loading_port_name or anchor_loading_port or eta_loading_port or etb_loading_port or ata_loading_port or atb_loading_port or etd_loading_port or atd_loading_port:
            loading_port = LoadingPort.objects.create(
                loading_port_name=loading_port_name,
                anchor_loading_port=anchor_loading_port,
                eta_loading_port=eta_loading_port,
                etb_loading_port=etb_loading_port,
                ata_loading_port=ata_loading_port,
                atb_loading_port=atb_loading_port,
                etd_loading_port=etd_loading_port,
                atd_loading_port=atd_loading_port,
                assigned_vessel_pol=vessel
            )
        
        # Guardar datos de DischargePort
        discharge_port_name = form.cleaned_data['discharge_port_name']
        anchor_discharge_port = form.cleaned_data['anchor_discharge_port']
        eta_discharge_port = form.cleaned_data['eta_discharge_port']
        etb_discharge_port = form.cleaned_data['etb_discharge_port']
        ata_discharge_port = form.cleaned_data['ata_discharge_port']
        atd_discharge_port = form.cleaned_data['atd_discharge_port']
        
        # Crea una instancia de DischargePort y la asocia con el Vessel
        if discharge_port_name or anchor_discharge_port or eta_discharge_port or etb_discharge_port or ata_discharge_port or atd_discharge_port:
            discharge_port = DischargePort.objects.create(
                discharge_port_name=discharge_port_name,
                anchor_discharge_port=anchor_discharge_port,
                eta_discharge_port=eta_discharge_port,
                etb_discharge_port=etb_discharge_port,
                ata_discharge_port=ata_discharge_port,
                atd_discharge_port=atd_discharge_port,
                assigned_vessel_pod=vessel
            )

        # Guardar datos de VesselAgent
        vessel_agent_name = form.cleaned_data['vessel_agent_name']
        vessel_agent_info = form.cleaned_data['vessel_agent_info']
        
        # Crea una instancia de VesselAgent y la asocia con el Vessel
        if vessel_agent_name or vessel_agent_info:
            vessel_agent = VesselAgent.objects.create(
                vessel_agent_name=vessel_agent_name,
                vessel_agent_info=vessel_agent_info,
                assigned_vessel=vessel
            )
        return super().form_valid(form)
    
"""

class VesselUpdate(UpdateView):
    model = Vessel
    template_name = "vessel_update.html"
    fields = "__all__"
    success_url = '/vessel/vessels-detail/{}/'

    def get_success_url(self):
        return reverse('VesselDetail', kwargs={'pk': self.object.pk}) + '?mensaje=Vessel+Successfully+Edited' 
        #'/vessel/vessels-detail/{}/'.format(self.object.pk) 

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.vessel_update(request, self.object.pk)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.vessel_update(request, self.object.pk)
    
    def vessel_update(self, request, pk):

        VesselToEdit = self.get_object()
    
        if request.method == 'POST':

            FormularioIngresado = self.get_form()
            FormularioIngresado = VesselPortsAgentFormset(request.POST, instance=VesselToEdit)
            loading_port_formset = VesselPortsAgentFormset.LoadingPortFormset(request.POST, instance=VesselToEdit)
            discharge_port_formset = VesselPortsAgentFormset.DischargePortFormset(request.POST, instance=VesselToEdit)
            vessel_agent_formset = VesselPortsAgentFormset.VesselAgentFormset(request.POST, instance=VesselToEdit)

            if FormularioIngresado.is_valid() and loading_port_formset.is_valid() and discharge_port_formset.is_valid() and vessel_agent_formset.is_valid():
                
                FormularioIngresado.save()
                VesselToEdit.save()
                loading_port_formset.save()
                discharge_port_formset.save()
                vessel_agent_formset.save()
                
                url = self.get_success_url() 
                return redirect(url)
            
            else:
              return render (request, "vessel_update.html", 
                             {"mensaje": "Invalid Form / Vessel Not Edited",
                              "FormularioIngresado": FormularioIngresado, 
                              "loading_port_formset": loading_port_formset,
                              "discharge_port_formset": discharge_port_formset,
                              "vessel_agent_formset": vessel_agent_formset,
                              "id": pk 
                              })
        else:
          FormularioIngresado = self.get_form()
          FormularioIngresado = VesselPortsAgentFormset (instance=VesselToEdit)
          loading_port_formset = VesselPortsAgentFormset.LoadingPortFormset(instance=VesselToEdit)
          discharge_port_formset = VesselPortsAgentFormset.DischargePortFormset(instance=VesselToEdit)
          vessel_agent_formset = VesselPortsAgentFormset.VesselAgentFormset(instance=VesselToEdit)

        return render (request, "vessel_update.html", 
                   {"FormularioIngresado": FormularioIngresado, 
                    "loading_port_formset": loading_port_formset,
                    "discharge_port_formset": discharge_port_formset,
                    "vessel_agent_formset": vessel_agent_formset,
                    "id": pk
                    })

"""
# 1 EDIT CON FORMULARIO MANUAL / FUNCIONA

def vessel_edit(request, id):

    VesselToEdit = Vessel.objects.get (id=id)
    
    if request.method == 'POST':

            FormularioIngresado = PruebaFormulario(request.POST)

            if FormularioIngresado.is_valid():

                data = FormularioIngresado.cleaned_data
                
                VesselToEdit.vessel_name = data["vessel_name"]
                VesselToEdit.vessel_imo = data ["vessel_imo"]
                VesselToEdit.save()
            
                return render (request, "vessel_edit.html", 
                               {"mensaje": "Vessel Edited", 
                                "id": VesselToEdit.id})
            
            else:
              #print(FormularioIngresado.errors)
              return render (request, "vessel_edit.html", 
                             {"mensaje": "Invalid Form / Vessel Not Edited", 
                              "id": VesselToEdit.id})
    else:
          FormularioIngresado = PruebaFormulario (initial=
                            {"vessel_name": VesselToEdit.vessel_name,
                            "vessel_imo": VesselToEdit.vessel_imo})
          #print (VesselToEdit.vessel_name)
        
    return render (request, "vessel_edit.html", 
                   {"FormularioIngresado": FormularioIngresado, 
                    "id": VesselToEdit.id})

"""

"""
#  2 EDIT CON INLINE FORMSET / FUNCIONA

def vessel_edit(request, id):

    VesselToEdit = Vessel.objects.get (id=id)
    
    if request.method == 'POST':

            FormularioIngresado = VesselPortsAgentFormset(request.POST, instance=VesselToEdit)
            loading_port_formset = VesselPortsAgentFormset.LoadingPortFormset(request.POST, instance=VesselToEdit)
            discharge_port_formset = VesselPortsAgentFormset.DischargePortFormset(request.POST, instance=VesselToEdit)
            vessel_agent_formset = VesselPortsAgentFormset.VesselAgentFormset(request.POST, instance=VesselToEdit)

            if FormularioIngresado.is_valid() and loading_port_formset.is_valid() and discharge_port_formset.is_valid() and vessel_agent_formset.is_valid():
                
                VesselToEdit.save()
                loading_port_formset.save()
                discharge_port_formset.save()
                vessel_agent_formset.save()
                
                url = reverse('VesselDetail', kwargs={'pk': id}) + '?mensaje=Vessel Successfully Edited'
                return redirect (url) 
                
            
            else:
              return render (request, "vessel_edit.html", 
                             {"mensaje": "Invalid Form / Vessel Not Edited",
                              "FormularioIngresado": FormularioIngresado, 
                              "loading_port_formset": loading_port_formset,
                              "discharge_port_formset": discharge_port_formset,
                              "vessel_agent_formset": vessel_agent_formset, 
                              "id": VesselToEdit.id})
    else:
          FormularioIngresado = VesselPortsAgentFormset (instance=VesselToEdit)
          loading_port_formset = VesselPortsAgentFormset.LoadingPortFormset(instance=VesselToEdit)
          discharge_port_formset = VesselPortsAgentFormset.DischargePortFormset(instance=VesselToEdit)
          vessel_agent_formset = VesselPortsAgentFormset.VesselAgentFormset(instance=VesselToEdit)

    return render (request, "vessel_edit.html", 
                   {"FormularioIngresado": FormularioIngresado, 
                    "loading_port_formset": loading_port_formset,
                    "discharge_port_formset": discharge_port_formset,
                    "vessel_agent_formset": vessel_agent_formset,
                    "id": VesselToEdit.id})
"""

class VesselDelete(DeleteView):
    model = Vessel
    tate_name = "vessel_delete.html"
    success_url = '/vessel/inicio/'






def prueba_formulario(request: HttpRequest):
    print ('method', request.method)
    print ('post', request.POST)

    if request.method == 'POST':
        
        FormularioIngresado = PruebaFormulario(request.POST)

        if FormularioIngresado.is_valid():

            print (FormularioIngresado.cleaned_data)

            data = FormularioIngresado.cleaned_data

            buque = Vessel(vessel_name=data ["vessel_name"], 
                           vessel_imo=data ["vessel_imo"]
                           )
            buque.save()

            FormularioNoIngresado = PruebaFormulario()

            return render (request, "prueba_formulario.html", 
                           {"FormularioIngresado": FormularioNoIngresado,
                           "mensaje": "Vessel Added"}
                           )
        else:
            return render (request, "prueba_formulario.html", 
                           {"mensaje": "Invalid Form / Vessel Not Added" }
                           )
    else:
     FormularioIngresado = PruebaFormulario()

     return render (request, "prueba_formulario.html", 
                       {"FormularioIngresado": FormularioIngresado}
                       )


def vessel_delete(request, id):
    
    if request.method == 'POST':
        
        VesselToDelete = Vessel.objects.get (id=id)

        if VesselToDelete:
            
            VesselToDelete.delete()

            vessels = Vessel.objects.all()
            
            return render (request, "vessel_delete.html", 
                           {"mensaje": "Vessel Successfully Deleted","vessels": vessels}
                           )
        else:
            return render (request, "vessel_delete.html", 
                           {"mensaje": "Invalid Form / Vessel Not Deleted" }
                           )
    else:
        vessels = Vessel.objects.all()
        return render (request, "vessel_delete.html", {"vessels": vessels})
    
