from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, login
from twilio.rest import Client
from django_otp.plugins.otp_totp.models import TOTPDevice
from dotenv import load_dotenv
import os
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

def home(request):
    return HttpResponse("hello world")

def register(request):
    if request.method == 'POST':
        print('hi')
        phone_number = request.POST.get('phone_number')
        phone_number="+91"+phone_number
        password = request.POST.get('password')

        User = get_user_model()
        user = User(phone_number=phone_number)
        user.set_password(password)
        user.save()

        # Create an OTP device for the user
        device = TOTPDevice(user=user, name=phone_number, confirmed=True)
        device.save()

        # Generate OTP code
        otp_code = device.generate_challenge()
        print(otp_code)
        if otp_code is None:
            user.delete()
            return render(request, 'register.html')

        # Send the OTP code via SMS
        client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        message = client.messages.create(
            body=f"Your OTP for registration: {otp_code}",
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to=phone_number
        )

        # Store the OTP code in the session for verification
        request.session['registration_otp_code'] = otp_code
        request.session['registration_phone_number'] = phone_number
        request.session['registration_password']=password
        try:
            return redirect('verify_otp')
        except:
            user.delete()
            return render(request, 'register.html')

    return render(request, 'register.html')

def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')

        # Retrieve the stored OTP code and phone number from the session
        stored_otp_code = request.session.get('registration_otp_code')
        phone_number = request.session.get('registration_phone_number')
        password=request.session.get('registration_password')
        if otp_code == stored_otp_code:
            # OTP verification successful
            User = get_user_model()
            user = User.objects.create_user(phone_number=phone_number)
            user.set_password(password)
            user.save()

            login(request, user)
            return redirect('dashboard')
        else:
            user.delete()  # Rollback the user creation
            return render(request, 'verify_otp.html', {'message': 'Invalid OTP code. Please try again.'})

    return render(request, 'verify_otp.html')

