from django.urls import path
from .views import TheatreAvailabilityView, CustomUnavailabilityView, SlotView

urlpatterns = [
    path('<int:id>/availability/', TheatreAvailabilityView.as_view(), name='theatre_availability'),
    path('<int:id>/custom-unavailability/', CustomUnavailabilityView.as_view(), name='custom_unavailability'),
    path('<int:id>/slots/', SlotView.as_view(), name='slots'),
]
