# rental/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CarFilterForm 
from .models import Car, Booking
from .forms import BookingForm

# Signup view for user registration
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = UserCreationForm()
    return render(request, 'rental/signup.html', {'form': form})

# Admin dashboard view (requires admin access)
def admin_dashboard(request):
    return render(request, 'rental/admin_dashboard.html')

# Customer dashboard view (view for customers to see their bookings and profile)
def customer_dashboard(request):
    return render(request, 'rental/customer_dashboard.html')

# View to list all available cars

def car_list(request):
    form = CarFilterForm(request.GET or None)
    qs = Car.objects.filter(available=True)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['make']:
            qs = qs.filter(make__iexact=cd['make'])
        if cd['model']:
            qs = qs.filter(model__iexact=cd['model'])
        if cd['price_min'] is not None:
            qs = qs.filter(price_per_day__gte=cd['price_min'])
        if cd['price_max'] is not None:
            qs = qs.filter(price_per_day__lte=cd['price_max'])
    return render(request, 'rental/car_list.html', {
        'form': form,
        'cars': qs,
    })


# Home page view (for the root URL)
def home(request):
    return render(request, 'rental/home.html')  # Create a home.html template in the templates folder

@login_required
def create_booking(request, car_id):
    car = get_object_or_404(Car, pk=car_id, available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            b = form.save(commit=False)
            b.car      = car
            b.customer = request.user
            b.save()
            return redirect('view_bookings')
    else:
        form = BookingForm()
    return render(request, 'rental/create_booking.html', {
        'car': car,
        'form': form,
    })
    
@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'rental/view_bookings.html', {
        'bookings': bookings,
    })

@staff_member_required
def manage_bookings(request):
    qs = Booking.objects.select_related('car', 'customer').order_by('-created_at')
    # optional: filter by ?status=confirmed / pending / etc
    status = request.GET.get('status')
    if status in dict(Booking.STATUS_CHOICES):
        qs = qs.filter(status=status)
    return render(request, 'rental/manage_bookings.html', {
        'bookings': qs,
        'status_choices': Booking.STATUS_CHOICES,
    })

@staff_member_required
def update_booking_status(request, booking_id, new_status):
    b = get_object_or_404(Booking, pk=booking_id)
    if new_status in dict(Booking.STATUS_CHOICES):
        b.status = new_status
        b.save()
    return redirect('manage_bookings')