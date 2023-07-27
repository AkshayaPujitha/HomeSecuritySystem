# myapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from dashboard.models import EventLog,Alarm,IntrusionImage

@receiver(post_save, sender=EventLog)
def delete_old_events(sender, instance, **kwargs):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    EventLog.objects.filter(timestamp=thirty_days_ago).delete()

@receiver(post_save, sender=Alarm)
def delete_old_events(sender, instance, **kwargs):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    Alarm.objects.filter(timestamp=thirty_days_ago).delete()

@receiver(post_save, sender=IntrusionImage)
def delete_old_events(sender, instance, **kwargs):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    IntrusionImage.objects.filter(timestamp=thirty_days_ago).delete()
