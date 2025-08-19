# orders/forms.py
from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'company_name', 'state',
            'street_address1', 'street_address2', 'city', 'division',
            'postcode', 'phone', 'order_note', 'payment_method'
        ]
