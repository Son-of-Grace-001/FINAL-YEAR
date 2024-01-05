# views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from allauth.account.views import SignupView
from .forms import CustomSignupForm, EditProfileForm
from .models import Department, CustomUser, Exeat, Upload, Amount, Complaint, Hostel, BedSpace
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
import requests
import os
import qrcode
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

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


@login_required
def complaint(request):
    user = request.user
    context = {
        'fname': user.first_name,
        'lname': user.last_name,
        'room_num': user.room,
        'block_num': user.block,
        'hostel': user.hostel
    }
    if request.method == 'POST':
        title = request.POST['title']
        block_number = request.POST['block_number']
        room_number = request.POST['room_number']
        message = request.POST['message']
        image = request.FILES['image']
        hostel_name = request.POST['hostel_name']
        fname = request.FILES['fname']
        lname = request.POST['lname']

        complaint = Complaint.objects.create(
            title=title,
            block_number=block_number,
            room_number=room_number,
            message=message,
            image=image,
            hostel_name=hostel_name,
            fname = fname,
            lname =lname
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

    return render(request, 'hostel/complaint.html', context)

@login_required
def book_pass(request):
    user = request.user
    context = {
        'fac': user.faculty,
        'dep': user.department,
        'level': user.level,
        'student_num': user.phone_number
    }
    
    if request.method == 'POST':
        departure_date = request.POST.get('departure_date')
        return_date = request.POST.get('return_date')
        reason = request.POST.get('reason')
        parent_number = request.POST ['parent_number']
        department = request.POST.get('department')
        faculty = request.POST.get('faculty')
        level = request.POST.get('level')
        student_number = request.POST ['student_number']

        exeat = Exeat.objects.create(
            user=request.user,
            departure_date=departure_date,
            return_date=return_date,
            reason=reason,
            parent_number = parent_number,
            faculty = faculty,
            department = department,
            level = level,
            student_number = student_number

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

    return render(request, 'hostel/book_pass.html', context)



def generate_pdf(instance):
    # Create a BytesIO buffer to store the PDF content
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file."
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 25)
    school_name = "Adeleke University Ede, Osun State"
    text_width = pdf.stringWidth(school_name, "Helvetica-Bold", 25)
    x_position = (letter[0] - text_width) / 2
    y_position = 750

    # Add the school name
    pdf.drawString(x_position, y_position, school_name)

    y_position -= 50

    pdf.setFont("Helvetica-Bold", 20)
    clearance_name = "Student's Exeact Clearance"
    text_width = pdf.stringWidth(clearance_name, "Helvetica-Bold", 20)
    x_position = (letter[0] - text_width) / 2
    y_position = 700

    # Add the school name
    pdf.drawString(x_position, y_position, clearance_name)

    # Set font and size for the content
    pdf.setFont("Helvetica", 11)

    # Add existing content to the PDF
    y_position -= 50

    # Add content to the PDF

    pdf.drawString(50, y_position, f'Hello, {instance.user.first_name} {instance.user.last_name}')
    y_position -= 40  # Adjust the y-coordinate for the next line
    pdf.drawString(50, y_position, f'Faculty: {instance.faculty}')
    y_position -= 40
    pdf.drawString(50, y_position, f'Department: {instance.department}')
    y_position -= 40
    pdf.drawString(50, y_position, f'Level: {instance.level}')
    y_position -= 40
    pdf.drawString(50, y_position, f'Student Number: {instance.student_number}')
    y_position -= 40
    pdf.drawString(50, y_position, f'Parent Number: {instance.parent_number}')
    y_position -= 40
    pdf.drawString(50, y_position, f'Reason: {instance.reason}')
    y_position -= 40
    pdf.drawString(50, y_position, f'Departure Date: {instance.departure_date}')
    y_position -= 40
    pdf.drawString(50, y_position, f'Return Date: {instance.return_date}')
    y_position -= 40
    pdf.drawString(50, y_position, f"Your exact request from {instance.departure_date} to {instance.return_date} has been {instance.status.title()} by an Admin")


    # Save the PDF to the buffer
    pdf.showPage()
    pdf.save()

    # File pointer to the beginning of the buffer
    buffer.seek(0)
    return buffer


def send_mail(instance):
    if instance.status == 'APPROVED':
        pdf_buffer = generate_pdf(instance)
        subject = "Exeat Request Approved"
    else:
        subject = "Exeat Request Rejected"
    body = f"Dear {instance.user.first_name} {instance.user.last_name} \n Faculty:{instance.user.faculty} \n Department: {instance.user.department} \n Parent Number: {instance.parent_number} \n Reason: {instance.reason} \n Your Exeat request from {instance.departure_date} to {instance.return_date} has been {instance.status.title()} by An Admin"
    mail = EmailMessage(subject= subject, body=body, from_email=settings.EMAIL_HOST_USER , to = [instance.user.email])
    if instance.status == 'APPROVED':
        mail.attach('Exeat.pdf', pdf_buffer.read(), 'application/pdf')
    mail.send()

@login_required
def upload_school_fee_evidence(request):
    # if user already have an hostel allocated to them, they should be redirected to home page
    if request.user.hostel or request.user.block or request.user.room:
        return redirect('dashboard')
    if request.method == 'POST':
        image = request.FILES['proof']
        payment_proof = Upload.objects.create(user=request.user, evidence=image)
        payment_proof.save()

        return redirect ('hostel_fees')
    return render (request, 'hostel/book_room.html')

@login_required
def book_room(request):
    user = request.user
    # if user already have an hostel allocated to them, they should be redirected to home page
    if user.hostel or user.block or user.room:
        return redirect('home')
    print(user.gender)
    if user.gender == 1:
        gender = 'male'
    else:
        gender = 'female'
    all_hostels = Hostel.objects.filter(gender=gender)
    if request.method == "POST":
        hostel_name = get_object_or_404(Hostel, name=request.POST.get("hostel-name"))
        bed_space = get_object_or_404(BedSpace, id=request.POST.get("space"))
        if bed_space.bunk.room.block.hostel != hostel_name:
            messages.info(request, "Invalid details")
            return redirect("book_room")
        if bed_space.is_allocated:
            messages.info(request, "Bed space not available")
            return redirect("book_room")
        bed_space.is_allocated = True
        bed_space.save()
    
        user.hostel = hostel_name
        user.block = bed_space.bunk.room.block
        user.room = bed_space.bunk.room
        user.bunk = bed_space.bunk
        user.space = bed_space
        user.save()

        
        # Generate PDF content and filename
        pdf_content, pdf_filename = get_pdf(user)

        # Construct the email subject and body
        subject = 'Room Allocation Confirmation'
        message = 'Thank you for booking a room. Please find your room allocation details in the attached PDF.'

        # Create the EmailMessage instance and attach the PDF
        email = EmailMessage(subject, message, to=[user.email])
        email.attach(pdf_filename, pdf_content.getvalue(), 'application/pdf')

        # Send the email
        email.send()

        messages.info(request, "Room Alocated successfully")
        return redirect('dashboard')

    available_spaces = []

    for hostel in all_hostels:
        all_bed_spaces = BedSpace.objects.filter(bunk__room__block__hostel=hostel)
        allocated_bed_spaces = all_bed_spaces.filter(is_allocated=True)
        available_bed_spaces = all_bed_spaces.exclude(pk__in=allocated_bed_spaces.values_list('pk', flat=True))
        available_spaces.append((hostel.name, available_bed_spaces))

    context = {
        'available_spaces': available_spaces
    }
    return render(request, 'hostel/allocate_room.html', context)

def get_pdf(user):
    # Create a BytesIO buffer to store the PDF content
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file."
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 25)
    school_name = "Adeleke University Ede, Osun State"
    text_width = pdf.stringWidth(school_name, "Helvetica-Bold", 25)
    x_position = (letter[0] - text_width) / 2
    y_position = 750

    # Add the school name
    pdf.drawString(x_position, y_position, school_name)

    y_position -= 40

    pdf.setFont("Helvetica-Bold", 20)
    clearance_name = "Student Hostel Clearance"
    text_width = pdf.stringWidth(clearance_name, "Helvetica-Bold", 25)
    x_position = (letter[0] - text_width) / 2
    y_position = 750

    # Add the school name
    pdf.drawString(x_position, y_position, clearance_name)

    # Set font and size for the content
    pdf.setFont("Helvetica", 18)

    # Add existing content to the PDF
    y_position -= 40

    # Add content to the PDF
    y_position = 800
    pdf.drawString(50, 800, f'Hello, {user.first_name} {user.last_name}')
    y_position -= 40
    pdf.drawString(50, 760, f'Hostel: {user.hostel}')
    y_position -= 40
    pdf.drawString(50, 720, f'Faculty: {user.faculty}')
    y_position -= 40
    pdf.drawString(50, 680, f'Department: {user.department}')
    y_position -= 40
    pdf.drawString(50, 640, f'Gender: {user.gender}')
    y_position -= 40
    pdf.drawString(50, 600, f'Block: {user.block}')
    y_position -= 40
    pdf.drawString(50, 560, f'Room: {user.room}')
    y_position -= 40
    pdf.drawString(50, 520, f'Bed Space: {user.space}')

    # Save the PDF to the buffer
    pdf.showPage()
    pdf.save()

    # Construct a filename for the PDF
    filename = f"{user.username}_room_allocation.pdf"

    # File pointer to the beginning of the buffer
    buffer.seek(0)

    return buffer, filename


@login_required
def hostel_fees(request):
    user = request.user
    # if user already have an hostel allocated to them, they should be redirected to home page
    if user.hostel or user.block or user.room:
        return redirect('dashboard')
    hostel_amount = Amount.objects.latest('price')
    context = {
        'user_email': user.email,
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
        'hostel_due': hostel_amount,
    }
    return render(request, 'hostel/hostel_fees.html', context)



