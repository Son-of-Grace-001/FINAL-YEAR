from django.forms import ModelChoiceField, ModelForm
from .models import Hostel, Room, Bunk, Block
# forms.py in your app

from allauth.account.forms import SignupForm
from django import forms
from .models import Faculty, Department, Gender, CustomUser
from django.core.validators import FileExtensionValidator, ValidationError

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    matric_number = forms.CharField(max_length=15, required=True)
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="Select Gender", required=True)
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), empty_label="Select Faculty", required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department", required=True)
    profile_image = forms.ImageField(validators=[
    FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])  # 1 MB limit

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'matric_number', 'department', 'profile_image']


    def save(self, request):
        # Call the original save method
        user = super().save(request)

        # Your additional save logic
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.matric_number = self.cleaned_data['matric_number']
        user.gender = self.cleaned_data['gender'].pk
        user.faculty = self.cleaned_data['faculty'].pk
        user.department = self.cleaned_data['department'].pk
        user.profile_image = self.cleaned_data['profile_image']

        user.save()

        # Ensure the user is marked as active after saving
        user.is_active = True
        user.save()

        return user


class EditProfileForm(ModelForm):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="Select Gender", required=True)
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), empty_label="Select Faculty", required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department", required=True)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_image', 'matric_number', 'faculty', 'gender', 'department']


