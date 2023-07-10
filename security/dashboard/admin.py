from django.contrib import admin
from .models import EventLog,Alarm,ImageUpload
# Register your models here.

admin.site.register(EventLog)
admin.site.register(Alarm)
admin.site.register(ImageUpload)

