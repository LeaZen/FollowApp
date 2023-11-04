from django.shortcuts import render
from .models import Vessel

# Create your views here.
def inicio (request):
    return render(request, "inicio.html")

def vessels_to_load (request):
    return render(request, "vessels_to_load.html")

def expected_arrivals (request):

    vesselsList = Vessel.objects.all()
    sorted_vesselsList = sorted(vesselsList, key=lambda x: x.eta_discharge_port)

    return render(request, "expected_arrivals.html", {"expected_arrivals":sorted_vesselsList})
