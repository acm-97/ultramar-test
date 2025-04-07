"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from .views import HomeView
from logistics.views import BookingListCreate, BookingRetrieveUpdateDestroy, VehicleListCreate, VehicleRetrieveUpdateDestroy

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="HomeView"),
    path('logistics/', include('logistics.urls'), name='logistics'),
    
    path('api/bookings/', BookingListCreate.as_view(), name='booking-list-create'),
    path('api/bookings/<int:pk>/', BookingRetrieveUpdateDestroy.as_view(), name='booking-update'),
    
    path('api/vehicles/', VehicleListCreate.as_view(), name='vehicle-list-create'),
    path('api/vehicles/<int:pk>/', VehicleRetrieveUpdateDestroy.as_view(), name='vehicle-update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)    
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
