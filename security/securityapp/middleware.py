from django.shortcuts import redirect

class VerifyOTPRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/verify_otp/' and not request.session.get('registration_phone_number'):
            return redirect('register')
        response = self.get_response(request)
        return response
