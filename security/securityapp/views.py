from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model, login
from twilio.rest import Client
from .serializers import UserSerializer,VerifyOTPSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dotenv import load_dotenv
import os
import pyotp

User = get_user_model()
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

def home(request):
    return HttpResponse("hello world")


@api_view(['POST','GET'])
def register(request):
    if request.method=='POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            
            # Generate a secret key for OTP
            secret_key = pyotp.random_base32()

            # Generate the OTP code
            totp = pyotp.TOTP(secret_key)
            otp_code = totp.now()

            
            user = User(phone_number=phone_number)
            user.set_password(password)
            user.save()

            # Send the OTP code to the user via SMS
            send_otp_code(phone_number, otp_code)
            request.session['registration_phone_number'] = phone_number
            request.session['crct_otp_code'] = otp_code

            return redirect('verify_otp')
        else:
            return Response(serializer.errors, status=400)
    else:
        return render(request,'register.html')
    


@api_view(['POST','GET'])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        otp_code = serializer.validated_data['otp_code']
        crct_code = request.session.get('crct_otp_code')
        phone_number = request.session.get('registration_phone_number')

        user = get_object_or_404(User, phone_number=phone_number)
        if otp_code == crct_code:
            login(request, user)
            return Response({'message': 'OTP verification successful. User logged in.'})
        else:
            user.delete()
            return Response({'error_message': 'Invalid OTP code'}, status=400)
   
    return render(request, 'verify_otp.html')



def send_otp_code(phone_number, otp_code):
    # Set up the Twilio client
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    client = Client(account_sid, auth_token)

    # Send the OTP code via SMS
    message = client.messages.create(
        body=f"Your OTP for registration: {otp_code}",
        from_=twilio_phone_number,
        to=phone_number
    )
