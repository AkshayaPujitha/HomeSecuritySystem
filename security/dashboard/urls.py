from django.urls import path,include
from .views import *
from . import views


app_name = 'dashboard'

urlpatterns=[
     path('',views.dashboard,name='dashboard'),
     path('stimulate/',views.simulate_events,name="stimulation"),
     path('upload/',views.upload,name="upload"),
     #path('get_images/',views.get_images,name="get")

]

