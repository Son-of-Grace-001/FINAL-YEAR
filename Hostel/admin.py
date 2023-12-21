from django.contrib import admin

# Register your models here.
# admin.py in your app

from django.contrib import admin
from .models import CustomUser

from .models import Faculty, Department,Amount, Gender, Hostel, Room, Block, Bunk, Position,Complaint, Exeat, Upload

admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Gender)
admin.site.register(CustomUser)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(Block)
admin.site.register(Bunk)
admin.site.register(Position)
admin.site.register(Complaint)
admin.site.register(Exeat)
admin.site.register(Upload)
admin.site.register(Amount)