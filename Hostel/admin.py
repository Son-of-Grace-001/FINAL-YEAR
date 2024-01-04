from django.contrib import admin

# Register your models here.
# admin.py in your app

from django.contrib import admin
from .models import CustomUser
from .models import Faculty, Department,Amount, Gender, Hostel, Room, Block, Bunk, BedSpace,Complaint, Exeat, Upload

class UserAdmin(admin.ModelAdmin):
  
    list_display = ('first_name', 'last_name', 'matric_number',
                    'faculty', 'department', 'gender',
                    'hostel', 'block', 'room', 'bunk', 'space')
    search_fields =  ('first_name', 'last_name', 'matric_number',
                    'faculty__name', 'department__name', 'gender__name',
                    'hostel__name', 'block__name', 'room__name', 'bunk__name', 'space__name')
    list_per_page = 20
admin.site.register(CustomUser, UserAdmin)


admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Gender)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(Block)
admin.site.register(Bunk)
admin.site.register(BedSpace)
admin.site.register(Complaint)
admin.site.register(Exeat)
admin.site.register(Upload)
admin.site.register(Amount)

