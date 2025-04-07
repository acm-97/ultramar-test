from django.shortcuts import render
from .models import Booking, Vehicle
from .serializers import BookingSerializer
from rest_framework import generics, filters
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import BookingForm
from django.core.paginator import Paginator

class BookingListCreate(generics.ListCreateAPIView):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer
  filter_backends = [filters.SearchFilter]
  search_fields = ['booking_number']
  
class BookingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
  
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
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return JsonResponse({'id': booking.id, 'booking_number': booking.booking_number, 'loading_port': booking.loading_port, 'discharge_port': booking.discharge_port, 'ship_arrival_date': booking.ship_departure_date, 'ship_arrival_date': booking.ship_departure_date})
        return JsonResponse({'error': 'Invalid data'}, status=400)

# Update a booking
def update_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save()
            return JsonResponse({'id': booking.id, 'booking_number': booking.booking_number, 'loading_port': booking.loading_port, 'discharge_port': booking.discharge_port, 'ship_arrival_date': booking.ship_departure_date, 'ship_arrival_date': booking.ship_departure_date})
        return JsonResponse({'error': 'Invalid data'}, status=400)

# Delete a booking
def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    return JsonResponse({'success': True})
      
  # def booking_create(request):

  # def vehicle_list(request):
  #     return render(request, "")