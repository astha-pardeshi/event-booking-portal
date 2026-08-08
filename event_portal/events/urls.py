from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='home'),name='logout'),
    path('book/<int:event_id>/',views.book_event, name='book_event'),
    
    path('my_booking/',views.my_bookings,name='my_bookings'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('dashboard/',views.dashboard,name='dashboard'),
    
    path('cancel-booking/<int:booking_id>/',views.cancel_booking,name='cancel_booking'),
    path('profile/',views.profile,name='profile'),
]