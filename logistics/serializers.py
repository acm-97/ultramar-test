from rest_framework import serializers
from .models import Booking, Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"
