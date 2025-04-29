# rental/models.py

from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=20)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)  # Image field for the car

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
