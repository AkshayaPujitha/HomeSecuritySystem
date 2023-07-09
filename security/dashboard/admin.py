from django.contrib import admin
from .models import EventLog,Alarm
# Register your models here.

admin.site.register(EventLog)
admin.site.register(Alarm)

