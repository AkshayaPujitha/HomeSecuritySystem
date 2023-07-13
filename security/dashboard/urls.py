from django.urls import path,include
from .views import *
from . import views


app_name = 'dashboard'

urlpatterns=[
     path('',views.dashboard,name='dashboard'),
     path('stimulate/',views.simulate_events,name="stimulation"),
     path('upload/',views.upload,name='upload'),
     path('detect/',views.detect,name='detect'),
     path('uploaded_images/',views.uploaded_images,name='uploaded_images'),

]

