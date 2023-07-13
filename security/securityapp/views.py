from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model, login,logout
from twilio.rest import Client
from .serializers import UserSerializer,VerifyOTPSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes
from rest_framework import generics,status
from dotenv import load_dotenv
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny

import os
import pyotp

User = get_user_model()
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

def home(request):
    return render(request,'home.html')

#Registration
@api_view(['POST','GET'])
@permission_classes([AllowAny])
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
            try:
            # Send the OTP code to the user via SMS
                send_otp_code(phone_number, otp_code)
                
            except:
                print(otp_code)
            request.session['registration_phone_number'] = phone_number
            request.session['crct_otp_code'] = otp_code

            return Response(status=status.HTTP_200_OK)
        else:
            print("here")
            return Response(serializer.errors, status=400)
    else:
        return render(request,'register.html')
    
#Function to Send OTP
def send_otp_code(phone_number, otp_code):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your OTP for registration: {otp_code}",
        from_=twilio_phone_number,
        to=phone_number
    )

#Verfication of OTP
@api_view(['POST','GET'])
def verify_otp(request):
    if request.method=='POST':
        serializer = VerifyOTPSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            crct_code = request.session.get('crct_otp_code')
            phone_number = request.session.get('registration_phone_number')
            user = get_object_or_404(User, phone_number=phone_number)
            if otp_code == crct_code:
                print(otp_code,crct_code)
                request.session['registration_phone_number'] = None
                request.session['crct_otp_code'] = None
                return Response(status=status.HTTP_200_OK)
            else:
                user.delete()
                return Response({'error': 'Invalid OTP code'}, status=400)
        else:
            request.session['registration_phone_number'] = None
            return Response({'error': 'Invalid OTP code'}, status=400)
   
    return render(request, 'verify_otp.html')


#Login
@api_view(['POST','GET'])
def login_view(request):
    if request.method=="POST":
        http_request = request._request
        phone_number= request.data.get('phone_number')
        password = request.data.get('password')
        try:
            user = User.objects.get(phone_number=phone_number)
            if user is not None and check_password(password, user.password):
                login(http_request,user)

                # Retrieve the token associated with the user
                token_obj,_ = Token.objects.get_or_create(user=user)
                response = {
                    "message":"Login Succesfully",
                    "token":token_obj.key
                }

                return Response(data=response,status=status.HTTP_200_OK)

                
            else:
                return Response({'error': 'Invalid Credentials Password invalid'}, status=400)
        except:
            return Response({'error': 'Phone Number doesnt exists'}, status=400)

    else:
        return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def trail(request):
    return render(request,'trail.html')