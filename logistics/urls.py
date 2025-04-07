from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingListCreate, BookingRetrieveUpdateDestroy, booking_list, create_booking, update_booking, delete_booking

# router = DefaultRouter()
# router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', booking_list, name="booking_list"),
    path('create/', create_booking, name='create_product'),
    path('update/<int:pk>/', update_booking, name='update_product'),
    path('delete/<int:pk>/', delete_booking, name='delete_product'),
    # path('api/', include(router.urls)),
]