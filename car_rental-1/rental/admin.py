from django.contrib import admin
from .models import Booking, Car, Profile, Payment

admin.site.register(Booking)
admin.site.register(Car)
admin.site.register(Profile)
admin.site.register(Payment)