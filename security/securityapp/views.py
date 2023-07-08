from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, login
from twilio.rest import Client
from django_otp.plugins.otp_totp.models import TOTPDevice
from dotenv import load_dotenv
import os
import pyotp

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

def home(request):
    return HttpResponse("hello world")

User = get_user_model()
def register(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        phone_number="+91"+phone_number
        user_all=User.objects.all()
        for user in user_all:
            if user.phone_number==phone_number:
                print("phone number already exists")
                return redirect('register')


        # Create a custom user
        user = User(phone_number=phone_number)
        user.set_password(password)
        user.save()

        # Generate a secret key for OTP
        secret_key = pyotp.random_base32()

        user.secret_key = pyotp.random_base32()  # Store the secret key directly on the user model
        user.save()


        # Generate the OTP code
        totp = pyotp.TOTP(user.secret_key)
        otp_code = totp.now()

        # Send the OTP code to the user via SMS
        send_otp_code(phone_number, otp_code)
        request.session['registration_phone_number'] = phone_number
        request.session['crct_otp_code'] = otp_code

        # Redirect to OTP verification page
        return redirect('verify_otp')

    return render(request, 'register.html')

def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        crct_code=request.session.get('crct_otp_code')
        print(otp_code,crct_code)
        phone_number = request.session.get('registration_phone_number')
        print(phone_number)

        # Retrieve the user based on the phone number
        user = User.objects.get(phone_number=phone_number)
        if user is None:
            return redirect('register')
        # Verify the OTP code
        if otp_code==crct_code:
            # OTP code is valid, log in the user
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
