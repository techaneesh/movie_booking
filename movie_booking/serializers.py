from rest_framework import serializers
from .models import *

class WeeklyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklySchedule
        fields = ['day', 'open_time', 'close_time']

class WeeklyUnavailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyUnavailability
        fields = ['day', 'start_time', 'end_time']

class CustomUnavailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUnavailability
        fields = ['date', 'start_time', 'end_time']

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['movie', 'start_time', 'end_time', 'is_available']
