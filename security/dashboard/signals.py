# myapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils.timezone import now, timedelta

from django.utils import timezone
from dashboard.models import EventLog,Alarm,IntrusionImage

@receiver(post_save, sender=EventLog)
def delete_old_events(sender, instance, **kwargs):
    thirty_days_ago = now() - timedelta(days=30)
    thirty_days_ago=thirty_days_ago.date()
    for event in EventLog.objects.all():
        if event.timestamp.date()<=thirty_days_ago:
            event.delete()
    

@receiver(post_save, sender=Alarm)
def delete_old_events(sender, instance, **kwargs):
    thirty_days_ago = now() - timedelta(days=30)
    thirty_days_ago=thirty_days_ago.date()
    for event in Alarm.objects.all():
        if event.timestamp.date()<=thirty_days_ago:
            event.delete()


@receiver(post_save, sender=IntrusionImage)
def delete_old_events(sender, instance, **kwargs):
    thirty_days_ago = now() - timedelta(days=30)
    thirty_days_ago=thirty_days_ago.date()
    for event in IntrusionImage.objects.all():
        if event.timestamp.date()<=thirty_days_ago:
            event.delete()
    