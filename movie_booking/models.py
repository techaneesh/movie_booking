from datetime import timedelta
from django.db import models

class Theatre(models.Model):
    name = models.CharField(max_length=100)

class Screen(models.Model):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='screens')
    name = models.CharField(max_length=100)

class WeeklySchedule(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='weekly_schedules')
    day = models.CharField(max_length=10)  # E.g., Monday, Tuesday
    open_time = models.TimeField()
    close_time = models.TimeField()

class WeeklyUnavailability(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='weekly_unavailabilities')
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

class CustomUnavailability(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='custom_unavailabilities')
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)

class Slot(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='slots')
    movie = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    day = models.CharField(max_length=10)  # To link with weekly schedules
    duration = models.DurationField(default=timedelta(hours=1))  # Default 1-hour slots
    is_available = models.BooleanField(default=True)
