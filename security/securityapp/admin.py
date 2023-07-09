from django.contrib import admin
from .models import CustomUser,EventLog,Alarm
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(EventLog)
admin.site.register(Alarm)

