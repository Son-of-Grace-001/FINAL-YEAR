from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


# Create your models here.
# models.py in your app

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    matric_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    hostel = models.ForeignKey('Hostel', on_delete=models.SET_NULL, null=True)
    block = models.ForeignKey('Block', on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username



class Hostel(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    # Add any other relevant fields

    def __str__(self):
        return self.name

class Block(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # Add any other relevant fields

    def __str__(self):
        return f"{self.hostel} - {self.name}"

class Room(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    number = models.IntegerField()
    name = models.CharField(max_length=10, default=1)
    # Add any other relevant fields

    def __str__(self):
        return f"{self.block} - Room {self.name}"

class Bunk(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models. CharField(max_length=10)
    # position = models.CharField(max_length=50)  # 'Up' or 'Down'
    # Add any other relevant fields

    def __str__(self):
        return f"{self.room} - Bunk {self.name} "

class Position(models.Model):
    bunk = models.ForeignKey(Bunk, on_delete=models.CASCADE, default='1')
    position = models.CharField(max_length=50)  # 'Up' or 'Down'
    def __str__(self):
        return f"{self.bunk} - Bunk {self.position}"

class Complaint (models.Model):
    title = models.CharField(max_length = 100)
    block_number = models.CharField(max_length = 100)
    room_number = models.CharField(max_length = 100)
    message = models.TextField()
    image = models.ImageField(upload_to='complaints_image')

    def __str__(self):
        return f"{self.title} - Room {self.room_number} in Block {self.block_number}"
    

class Exeat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent_number = models.IntegerField( )
    departure_date = models.DateField()
    return_date = models.DateField()
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.departure_date} to {self.return_date}"
    
class Upload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evidence = models.ImageField(upload_to = 'evidence-of-payment')
    
    def __str__ (self):
        return  f"{self.user} - {self.evidence}"


class Amount(models.Model):
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.price}"
