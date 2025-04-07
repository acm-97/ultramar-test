from rest_framework import serializers
from .models import Booking, Vehicle

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    booking = BookingSerializer()
    
    class Meta:
        model = Vehicle
        fields = "__all__"
