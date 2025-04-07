from django import forms
from .models import Booking, Vehicle

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_number', 'loading_port', 'discharge_port', 'ship_arrival_date', 'ship_departure_date']
        
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vin', 'make', 'model', 'weight', 'booking_id']