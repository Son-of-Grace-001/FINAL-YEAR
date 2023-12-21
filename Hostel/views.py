# views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from allauth.account.views import SignupView
from .forms import CustomSignupForm, EditProfileForm
from .models import Department, CustomUser, Exeat, Upload, Amount
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests

def home (request):
  return render (request, 'hostel/home.html')

@login_required
def dashboard (request):
  user = request.user
  return render (request, 'hostel/dashboard.html')


class CustomSignupView(SignupView):
    form_class = CustomSignupForm

def custom_logout(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            # The form is valid, continue with saving
            user = form.save(request)
            # Additional logic after saving
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        form = CustomSignupForm()

    return render(request, 'account/signup.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the user's profile page
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'hostel/edit_profile.html', {'form': form})

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Complaint

@login_required
def complaint(request):
    if request.method == 'POST':
        title = request.POST['title']
        block_number = request.POST['block_number']
        room_number = request.POST['room_number']
        message = request.POST['message']
        image = request.FILES['image']

        complaint = Complaint.objects.create(
            title=title,
            block_number=block_number,
            room_number=room_number,
            message=message,
            image=image
        )
        complaint.save()

        if request.user.is_authenticated:
            user_first_name = request.user.first_name
            user_last_name = request.user.last_name
            user_email = request.user.email
        else:
            user_first_name = 'Guest'
            user_last_name = ''
            user_email = 'example@example.com'
        
        subject = "Thanks for contacting us"
        body = f"Hello {user_first_name} {user_last_name},\n\nThank you for reaching out to us, your message has been received successfully, we will get back to you as soon as possible\n\nWarm Regards,\n\n Adeleke Hostel Admin\n"

        mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [user_email])
        mail.send()
        
        subject = "New message Alert"
        body = f"A new message was received from {user_first_name} {user_last_name}, on {block_number} blobk, room {room_number}, with the message of '{message}', and a mail has been automatically sent to their eamil, which is {user_email} Please attend to it"
        
        mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [settings.EMAIL_HOST_USER])
        mail.send()
        messages.info(request, "Your message was sent successfully")

        messages.success(request, 'Complaint submitted successfully.')
        return redirect('dashboard')  # Redirect to a success page

    return render(request, 'hostel/complaint.html')

@login_required
def book_pass(request):
    if request.method == 'POST':
        departure_date = request.POST.get('departure_date')
        return_date = request.POST.get('return_date')
        reason = request.POST.get('reason')
        parent_number = request.POST ['parent_number']

        exeat = Exeat.objects.create(
            user=request.user,
            departure_date=departure_date,
            return_date=return_date,
            reason=reason,
            parent_number = parent_number
        )
        exeat.save()

        if request.user.is_authenticated:
            user_first_name = request.user.first_name
            user_last_name = request.user.last_name
            user_email = request.user.email
        else:
            user_first_name = 'Guest'
            user_last_name = ''
            user_email = 'example@example.com'
        # Send email notification to the student
        subject = "Exeat Request Submitted"
        body = f"Your Exeat request from {departure_date} to {return_date} has been submitted. You will receive a confirmation once it is approved or declined."
        mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [user_email])
        mail.send()


        subject = "New Exeat Alert"
        body = f"A new Exeat was received from {user_first_name} {user_last_name}, to leave the school from {departure_date} to {return_date}, with the reason '{reason}', and a mail has been automatically sent to their eamil, which is {user_email} Please attend to it."
        mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [settings.EMAIL_HOST_USER])
        mail.send()

        messages.success(request, 'Exeat request submitted successfully.')
        return redirect('dashboard')

    return render(request, 'hostel/book_pass.html')

@login_required
def book_room(request):
    if request.method == 'POST':
        image = request.FILES['proof']
        payment_proof = Upload.objects.create(user=request.user, evidence=image)
        payment_proof.save()

        return redirect ('hostel_fees')
    return render (request, 'hostel/book_room.html')


@login_required
def hostel_fees(request):
    user = request.user
    hostel_amount = Amount.objects.latest('price')
    context = {
        'user_email': user.email,
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
        'hostel_due': hostel_amount,
    }
    return render(request, 'hostel/hostel_fees.html', context)

# @csrf_exempt
# def paystack_callback(request):
#     # Retrieve information from Paystack callback
#     reference = request.POST.get('data[reference]')
#     amount_paid = request.POST.get('data[amount]')

#     # Verify payment status using Paystack API
#     paystack_verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
#     headers = {'Authorization': 'Bearer YOUR_PAYSTACK_SECRET_KEY'}
#     response = requests.get(paystack_verify_url, headers=headers)
#     data = response.json()

#     # Check if payment was successful
#     if data['status'] and data['data']['status'] == 'success':
#         # Payment was successful, perform additional logic if needed
#         # For example, update your database, generate a booking, etc.

#         # Retrieve the latest amount from your Amount model
#         latest_amount = Amount.objects.latest('created')

#         # Redirect to a template with the latest_amount information
#         return render(request, 'your_template.html', {'latest_amount': latest_amount})

#     # Payment was not successful, handle accordingly
#     return HttpResponse("Payment failed")


