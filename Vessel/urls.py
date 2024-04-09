from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('inicio/', inicio, name= 'follow app'),
    path('vessels-to-load/', vessels_to_load, name= 'vessels to load'),
    path('expected-arrivals/', expected_arrivals, name= 'expected arrivals'),
    #path('loading-port-detail/', loading_port_detail, name= 'loading port detail'),

    path('vessels-list/', VesselList.as_view(), name= 'VesselList'),
    path('vessels-detail/<pk>', VesselDetail.as_view(), name= 'VesselDetail'),
    path('vessels-create/', VesselCreate.as_view(), name= 'VesselCreate'),
    
    path('vessels-update/<pk>', VesselUpdate.as_view(), name= 'VesselUpdate'),
    path('vessels-delete/<pk>', VesselDelete.as_view(), name= 'VesselDelete'),
    path('prueba-formulario/', prueba_formulario, name= 'PruebaFormulario'),

    path('search-vessel/', search_vessel, name= 'SearchVessel'),
        
]