from django.shortcuts import render,redirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes,authentication_classes,api_view
from rest_framework.permissions import IsAuthenticated
from .models import EventLog,Alarm,ImageUpload,IntrusionImage
from django.http import HttpResponse
import random
import datetime
from django.utils import timezone
import cv2
import face_recognition
import os
from django.conf import settings
import numpy as np
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from twilio.rest import Client
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import numpy as np
import uuid

User = get_user_model()
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
#@authentication_classes([TokenAuthentication])
def dashboard(request):
    return render(request,'dashboard.html')


def simulate_events(request):
    event_types = ['glass_break', 'door_opened', 'smoke_detector']
    num_events = random.randint(1, 3)
    events = []
    for _ in range(num_events):
        event_type = random.choice(event_types)
        event_time = generate_random_timestamp()
        user=request.user
        event = EventLog.objects.create(user=user,event_type=event_type, timestamp=event_time)
        events.append(event)
        if event_type == 'glass_break':
            pass
        elif event_type == 'door_opened':
            pass
        elif event_type == 'smoke_detector':
            trigger_smoke_detector_alarm(user,event_time,event)
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

##To Upload images
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def upload(request):
    if request.method=='POST':
        img=request.FILES.get('image')
        print(img)
        name=request.POST.get('name')
        user=request.user
        ImageUpload.objects.create(user=user,image=img,name=name)
        return render(request,'upload_images.html')
    return render(request,'upload_images.html')

    
#Webcam
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detect(request):
    user=request.user
    encodeList,id=encodings(user)
    #print(encodeList,id)
    intruder=0
    cap=cv2.VideoCapture(0)
    i=0
    cnt=0
    while i<200 :
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
                intruder=frame
                cnt+=1
                print("Unknown face detected")
    
        i+=1
    print(cnt)
   # print(intruder)
    if cnt>=40:
        event_time = generate_random_timestamp()
        event=EventLog.objects.create(user=user,timestamp=event_time,event_type="Unknown Face Detected")
        trigger_intrusion_alarm(request.user,event)
        save_image(intruder,request.user)

    return render(request,"dashboard.html")


#Encodings of Images Uploaded by user   
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

def trigger_intrusion_alarm(user,event):
    Alarm.objects.create(user=user,event_log=event,alarm_type="Intrusion",timestamp=generate_random_timestamp())
    print("store image and send in dash board and alarm it")
    try:
        message="An unknow face detected Ceck the website for more info<WEBSITE LINK> "
        send_sms(user,message)
    except:
        pass
    
    return 

#Sends SMS to only verified numbers of twilio
def send_sms(user,message):
    phone_number=user.phone_number
    phone_number='+91'+phone_number
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    twilio_phone_number = TWILIO_PHONE_NUMBER
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your OTP for registration: {message}",
        from_=twilio_phone_number,
        to=phone_number
    )

def save_image(intruder,user):
    image = Image.fromarray(intruder)
    image_io = BytesIO()
    image.save(image_io, format='JPEG') 
    content_file = ContentFile(image_io.getvalue())
    filename = f'intruder_image{uuid.uuid4()}.jpg'
    intrusion_image = IntrusionImage.objects.create(image=filename, user=user,timestamp=generate_random_timestamp())
    intrusion_image.image.save('image.jpg', content_file)



    





    


