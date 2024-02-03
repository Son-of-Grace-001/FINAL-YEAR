import pyotp
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime, timedelta

def send_otp(request):
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        # Access the authenticated user's email
        user_email = request.user.email

        # Generate OTP
        totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
        otp = totp.now()

        # Store OTP and expiration date in session
        request.session['otp_secret_key'] = totp.secret
        valid_date = datetime.now() + timedelta(minutes=5)
        request.session['otp_valid_date'] = str(valid_date)

        # Send OTP via email (replace with your own email sending logic)
        # subject = 'Your One Time Password'
        # body =f'Your one-time password is: {otp}. This OTP is valid until {valid_date}.'
        # mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [user_email])
        # mail.send()

        print (f'Your one-time password is: {otp}.')
    else:
        return HttpResponse("User is not authenticated.")
