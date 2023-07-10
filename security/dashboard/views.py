from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes,authentication_classes,api_view
from rest_framework.permissions import IsAuthenticated
from .models import EventLog,Alarm,ImageUpload
from django.http import HttpResponse
import random
import datetime
from django.utils import timezone
import cv2
import face_recognition
from django.core.files.storage import default_storage
import os
from django.conf import settings
import numpy as np




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

def upload(request):
    if request.method=='POST':
        img=request.FILES.get('image')
        print(img)
        name=request.POST.get('name')
        user=request.user
        ImageUpload.objects.create(user=user,image=img,name=name)
        return HttpResponse("Uploaded Sucessfully")
#Webcam
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detect(request):
    user=request.user
    encodeList,id=encodings(user)
    #print(encodeList,id) 
    cap=cv2.VideoCapture(0)
    i=0
    cnt=0
    while i<500 :
        ret,frame=cap.read()
        imgS=cv2.resize(frame,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
        faceCurFrame=face_recognition.face_locations(imgS)
        encodingCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)
        for encodeFace,faceLoc in zip(encodingCurFrame,faceCurFrame):
            matches=face_recognition.compare_faces(encodeList,encodeFace)
            faceDist=face_recognition.face_distance(encodeList,encodeFace)
            print(matches,faceDist)
            ind=np.argmin(faceDist)
            if not matches[ind]:
                cnt+=1
                print("Unknown face detected")
    
        i+=1
    print(cnt)
    if cnt>=50:
        event_time = generate_random_timestamp()
        EventLog.objects.create(user=user,timestamp=event_time,event_type="Unknown Face Detected")


    return HttpResponse("succeed")   


    
def encodings(user):
    images = ImageUpload.objects.filter(user=user)
    imgList=[]
    ids=[]
    for image in images:
        image_path = settings.MEDIA_ROOT +'/'+str(image.image)
        ids.append(image.id)
        imgList.append(cv2.imread(image_path))
    encodeList=[]
    idList=[]
    for image,id in zip(imgList,ids):
        #print(id)
        img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        encodings=face_recognition.face_encodings(img)
        if encodings:
            encodeList.append(encodings[0])
            idList.append(id)
    return encodeList,idList
    





    


