from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, login
from twilio.rest import Client
from .serializers import UserSerializer
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
    



def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        crct_code=request.session.get('crct_otp_code')
        print(otp_code,crct_code)
        phone_number = request.session.get('registration_phone_number')
        print(phone_number)

        
        user = User.objects.get(phone_number=phone_number)
        if user is None:
            return redirect('register')
        
        if otp_code==crct_code:
            login(request, user)
            try:
                return redirect('dashboard')
            except:
                return render(request,'dashboard.html')
        else:
            user.delete()
            # OTP code is invalid, display an error message
            return render(request, 'verify_otp.html', {'error_message': 'Invalid OTP code'})

    # Store the phone number in the session
    phone_number = request.session.get('registration_phone_number')
    if not phone_number:
        return redirect('register')

    return render(request, 'verify_otp.html', {'phone_number': phone_number})



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
