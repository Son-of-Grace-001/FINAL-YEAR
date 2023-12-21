from django.urls import path
from . import views




urlpatterns = [
    # Other URL patterns
    path ('', views.home, name='home'),
    path ('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.custom_logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('complaint/', views.complaint, name='complaint'),
    path('bookpass/', views.book_pass, name='pass'),
    # path('payment/', views.book_room, name='upload'),
    path('fee/', views.hostel_fees, name= 'hostel_fees'),
    path('pay/', views.book_room, name= 'payment'),
    #  path('paystack/callback/', views.paystack_callback, name='paystack_callback'),
   
    # Other URL patterns...
]
