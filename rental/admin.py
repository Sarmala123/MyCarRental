from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display    = ('car', 'customer', 'start_date', 'end_date', 'status')
    list_filter     = ('status', 'start_date', 'end_date', 'customer__username')
    search_fields   = ('customer__username', 'car__make', 'car__model')
