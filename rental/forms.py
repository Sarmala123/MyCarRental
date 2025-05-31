from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Car, Booking
from .models import Payment
from .models import Profile

class CarFilterForm(forms.Form):
    make = forms.CharField(required=False, label='Make')
    model = forms.CharField(required=False, label='Model')
    price_min = forms.DecimalField(
        required=False, label='Min price / day', min_value=0
    )
    price_max = forms.DecimalField(
        required=False, label='Max price / day', min_value=0
    )

    def filter_queryset(self, qs):
        if not self.is_valid():
            return qs
        cd = self.cleaned_data
        if cd['make']:
            qs = qs.filter(make__icontains=cd['make'])
        if cd['model']:
            qs = qs.filter(model__icontains=cd['model'])
        if cd['price_min'] is not None:
            qs = qs.filter(price_per_day__gte=cd['price_min'])
        if cd['price_max'] is not None:
            qs = qs.filter(price_per_day__lte=cd['price_max'])
        return qs

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date':   forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Expect `car` kwarg passed from the view
        self.car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        booking = super().save(commit=False)
        if self.car:
            booking.car = self.car
        if commit:
            booking.save()
        return booking

    def clean(self):
        cleaned = super().clean()
        s = cleaned.get('start_date')
        e = cleaned.get('end_date')
        if not (s and e):
            return cleaned
        if s < date.today():
            self.add_error('start_date', 'Start date cannot be in the past.')
        if e < s:
            self.add_error('end_date', 'End date must be after start.')
        # Check overlapping bookings
        overlaps = Booking.objects.filter(
            car=self.car,
            status__in=[Booking.PENDING, Booking.CONFIRMED],
            start_date__lte=e,
            end_date__gte=s,
        )
        if overlaps.exists():
            raise forms.ValidationError('This car is already booked for those dates.')
        return cleaned


class SignUpForm(UserCreationForm):
    """Create user but keep them inactive until admin approval."""
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False         # <-- NEW: block login until approved
        if commit:
            user.save()
        return user

class MockPaymentForm(forms.ModelForm):
    """
    Very simple “pretend card” form: card number & name.
    """
    card_number = forms.CharField(max_length=19, label="Card number")
    card_name   = forms.CharField(max_length=40, label="Name on card")

    class Meta:
        model  = Payment
        fields = []  


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo"]