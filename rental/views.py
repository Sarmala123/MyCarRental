# rental/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Car

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
    cars = Car.objects.filter(available=True)  # List of available cars
    return render(request, 'rental/car_list.html', {'cars': cars})

# Home page view (for the root URL)
def home(request):
    return render(request, 'rental/home.html')  # Create a home.html template in the templates folder
