from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from .models import Event,Booking
from .forms import RegisterForm
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required



def home(request):
    query = request.GET.get('q')

    if query:
        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    else:
        events = Event.objects.all()

    return render(request, 'home.html', {
        'events': events,
        'query': query
    })



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

class UserLoginView(LoginView):
    template_name = "login.html"
    next_page = "/"
    
    
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        print("BOOKING POST RECEIVED")
        
        Booking.objects.create(
            user=request.user,
            event=event,
            tickets=1
        )

        return redirect('my_bookings')

    return render(
        request,
        "confirm_booking.html",
        {"event": event}
    )


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "my_bookings.html", {"bookings": bookings})

def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


from django.contrib.auth.models import User

@login_required
def dashboard(request):
    total_events = Event.objects.count()
    total_bookings = Booking.objects.count()
    total_users = User.objects.count()

    recent_bookings = Booking.objects.select_related(
        "user", "event"
    ).order_by("-booking_date")[:5]

    context = {
        "total_events": total_events,
        "total_bookings": total_bookings,
        "total_users": total_users,
        "recent_bookings": recent_bookings,
    }

    return render(request, "dashboard.html", context)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('my_bookings')

@login_required
def profile(request):
    return render(request, "profile.html")

# Create your views here.
