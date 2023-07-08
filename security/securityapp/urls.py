from django.urls import path,include
from .views import *
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('',views.home,name="home"),
    path('gettoken/',obtain_auth_token),
    path('register/', views.register, name='register'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('login/',views.login,name="login"),
    path('dashboard/',views.dashboard,name='dashboard')
    
]