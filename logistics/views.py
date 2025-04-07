from django.shortcuts import render
from .models import Booking, Vehicle
from .serializers import BookingSerializer, VehicleSerializer
from rest_framework import generics, filters
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import BookingForm, VehicleForm
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import authentication, permissions

class BookingListCreate(generics.ListCreateAPIView):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ['booking_number']
  
class BookingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
  
# Get the bookling list
@api_view(['GET'])
@permission_classes([AllowAny])
def booking_list(request):
    query = request.GET.get('search', '')
    sort = request.GET.get('sort', 'id')  # default sort
    order = request.GET.get('order', 'asc')
    page = int(request.GET.get('page', 1))
    per_page = 5

    sort_prefix = '' if order == 'asc' else '-'
    bookings = Booking.objects.filter(booking_number__icontains=str(query)).order_by(f'{sort_prefix}{sort}') if query else Booking.objects.all()

    paginator = Paginator(bookings, per_page)
    page_obj = paginator.get_page(page)
    
    serializer = BookingSerializer(page_obj.object_list, many=True)
    
    context = {
        "query": query,
        'results': serializer.data,
        'total': paginator.count,
        'page_range': range(paginator.num_pages),
        'pages': paginator.num_pages,
        'current_page': page,
    }
    return render(request, "bookings/bookings_list.html", context)
  
# Create a booking
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    form = BookingForm(request.POST)
    if form.is_valid():
        booking = form.save()
        return JsonResponse({'id': booking.id, 'booking_number': booking.booking_number, 'loading_port': booking.loading_port, 'discharge_port': booking.discharge_port, 'ship_arrival_date': booking.ship_departure_date, 'ship_arrival_date': booking.ship_departure_date})
    return JsonResponse({'error': 'Invalid data'}, status=400)

# Update a booking
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST, instance=booking)
    if form.is_valid():
        booking = form.save()
        return JsonResponse({'id': booking.id, 'booking_number': booking.booking_number, 'loading_port': booking.loading_port, 'discharge_port': booking.discharge_port, 'ship_arrival_date': booking.ship_departure_date, 'ship_arrival_date': booking.ship_departure_date})
    return JsonResponse({'error': 'Invalid data'}, status=400)

# Delete a booking
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    return JsonResponse({'success': True})
      

# VEHICLE VIEWS ---------------------------------------------------------------------------------
class VehicleListCreate(generics.ListCreateAPIView):
  queryset = Vehicle.objects.all()
  serializer_class = VehicleSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ['vin']
  
class VehicleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    lookup_field = 'pk'

@api_view(['GET'])
@permission_classes([AllowAny])
def vehicle_list(request):
    bookings = Booking.objects.all()
    query = request.GET.get('search', '')
    sort = request.GET.get('sort', 'id')  # default sort
    order = request.GET.get('order', 'asc')
    page = int(request.GET.get('page', 1))
    per_page = 5

    sort_prefix = '' if order == 'asc' else '-'
    vehicles = Vehicle.objects.filter(vin__icontains=str(query)).order_by(f'{sort_prefix}{sort}') if query else Vehicle.objects.all()

    paginator = Paginator(vehicles, per_page)
    page_obj = paginator.get_page(page)
    
    serializer = VehicleSerializer(page_obj.object_list, many=True)
    
    context = {
        "query": query,
        'results': serializer.data,
        'total': paginator.count,
        'page_range': range(paginator.num_pages),
        'pages': paginator.num_pages,
        'current_page': page,
        'bookings': bookings
    }
    return render(request, "vehicles/vehicles_list.html", context)
  
# Create a vehicle
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vehicle(request):
    form = VehicleForm(request.POST)
    if form.is_valid():
        vehicle = form.save()
        return JsonResponse({'id': vehicle.id, 'vin': vehicle.vin, 'make': vehicle.make, 'model': vehicle.model, 'weight': vehicle.weight, 'booking': vehicle.booking})
    return JsonResponse({'error': 'Invalid data'}, status=400)

# Update a vehicle
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    form = VehicleForm(request.POST, instance=vehicle)
    if form.is_valid():
        vehicle = form.save()
        return JsonResponse({'id': vehicle.id, 'vin': vehicle.vin, 'make': vehicle.make, 'model': vehicle.model, 'weight': vehicle.weight, 'booking': vehicle.booking})
    return JsonResponse({'error': 'Invalid data'}, status=400)

# Delete a vehicle
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    return JsonResponse({'success': True})