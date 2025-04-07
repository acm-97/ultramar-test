from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_number', 'loading_port', 'discharge_port', 'ship_arrival_date', 'ship_departure_date']