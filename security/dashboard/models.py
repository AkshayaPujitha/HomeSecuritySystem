from django.db import models
from django.contrib.auth import get_user_model


User=get_user_model()

class EventLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type=models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return self.event_type

class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alarm_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    event_log = models.ForeignKey(EventLog, on_delete=models.CASCADE)

    def __str__(self):
        return self.alarm_type

class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    images=models.ImageField(blank=False)

