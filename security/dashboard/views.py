from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes,authentication_classes,api_view
from rest_framework.permissions import IsAuthenticated
from .models import EventLog,Alarm
from django.http import HttpResponse
import random
import datetime
from django.utils import timezone



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    return render(request,'dashboard.html')

# Function to simulate events
def simulate_events(request):
    event_types = ['glass_break', 'door_opened', 'smoke_detector']

    # Generate a random number of events (1 to 3)
    num_events = random.randint(1, 3)

    # Generate events
    events = []
    for _ in range(num_events):
        event_type = random.choice(event_types)
        event_time = generate_random_timestamp()
        user=request.user
        # Create the event object
        event = EventLog.objects.create(user=user,event_type=event_type, timestamp=event_time)
        events.append(event)

        # Check if the event triggers an alarm
        if event_type == 'glass_break':
            pass
            #trigger_glass_break_alarm()
        elif event_type == 'door_opened':
            pass
            #trigger_door_opened_alarm()
        elif event_type == 'smoke_detector':
            trigger_smoke_detector_alarm(user,event_time,event)

    # Return the created event objects
    return HttpResponse("hello")

def trigger_smoke_detector_alarm(user,event_time,event):
    Alarm.objects.create(user=user,timestamp=event_time,event_log=event,alarm_type="Alarm of Smoke detector")

# Function to generate a random timestamp within the past hour
def generate_random_timestamp():
    now = timezone.now()
    start_time = now - datetime.timedelta(hours=1)
    return random_date(start_time, now)

# Function to generate a random date/time within a range
def random_date(start, end):
    delta = end - start
    random_second = random.randint(0, delta.total_seconds())
    return start + datetime.timedelta(seconds=random_second)

# Functions to trigger alarms
# ...

# Call the simulate_events() function to simulate events

