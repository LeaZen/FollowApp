from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('inicio/', inicio, name= 'follow app'),
    path('vessels-to-load/', vessels_to_load, name= 'vessels to load'),
    path('expected-arrivals/', expected_arrivals, name= 'expected arrivals'),
]