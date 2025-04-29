# rental/admin.py

from django.contrib import admin
from .models import Car  # Import the Car model

# Register the Car model so it appears in the admin panel
admin.site.register(Car)
