from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('api/theatre/', include('movie_booking.urls')),  # Routes all requests for movie_booking
]
