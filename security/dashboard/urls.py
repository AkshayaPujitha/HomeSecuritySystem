from django.urls import path,include
from .views import *
from . import views

app_name = 'dashboard'

urlpatterns=[
     path('',views.dashboard,name='dashboard'),
     path('stimulate/',views.simulate_events,name="stimulation")
]