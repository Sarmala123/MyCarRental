# rental/forms.py

from django import forms

class CarFilterForm(forms.Form):
    make = forms.CharField(max_length=100, required=False)
    model = forms.CharField(max_length=100, required=False)
    price_min = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    price_max = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
