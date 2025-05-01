# rental/models.py

from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=20)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)  # Image field for the car
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled',  'Canceled'),
    ]
    car         = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer    = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date  = models.DateField()
    end_date    = models.DateField()
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
