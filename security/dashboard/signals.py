# myapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from dashboard.models import EventLog

@receiver(post_save, sender=EventLog)
def delete_old_events(sender, instance, **kwargs):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    EventLog.objects.filter(timestamp=thirty_days_ago).delete()
