from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Theatre, Screen, Slot, WeeklySchedule, WeeklyUnavailability, CustomUnavailability
from .serializers import SlotSerializer
from datetime import datetime, timedelta

class TheatreAvailabilityView(APIView):
    def post(self, request, id):
        theatre = Theatre.objects.get(id=id)

        # Save weekly schedule
        weekly_schedule_data = request.data.get('weekly_schedule', {})
        for day, times in weekly_schedule_data.items():
            open_time = times['open']
            close_time = times['close']

            for screen in theatre.screens.all():  # Iterate over screens of the theatre
                # Update or create weekly schedule for each screen
                WeeklySchedule.objects.update_or_create(
                    screen=screen, day=day,
                    defaults={'open_time': open_time, 'close_time': close_time}
                )

                # Dynamically generate slots for the day
                self.generate_slots(screen, day, open_time, close_time)

        # Save weekly unavailability
        weekly_unavailability_data = request.data.get('weekly_unavailability', {})
        for day, periods in weekly_unavailability_data.items():
            for period in periods:
                for screen in theatre.screens.all():
                    WeeklyUnavailability.objects.update_or_create(
                        screen=screen, day=day,
                        defaults={'start_time': period['start'], 'end_time': period['end']}
                    )

        return Response({'message': 'Theatre availability updated.'}, status=status.HTTP_200_OK)

    def generate_slots(self, screen, day, open_time, close_time):
        # Delete existing slots for this screen and day to avoid duplicates
        Slot.objects.filter(screen=screen, day=day).delete()

        current_time = datetime.strptime(open_time, "%H:%M")
        end_time = datetime.strptime(close_time, "%H:%M")
        delta = timedelta(minutes=60)

        # Generate slots between opening and closing times
        while current_time < end_time:
            start_time = current_time
            current_time += delta
            end_time_slot = current_time

            Slot.objects.create(
                screen=screen,
                movie="Available Slot",  # Placeholder
                day=day,
                start_time=start_time,
                end_time=end_time_slot,
                is_available=True
            )


class CustomUnavailabilityView(APIView):
    def post(self, request, id):
        screen = Screen.objects.get(id=request.data['screen_id'])

        # Save unavailable slots
        unavailable_slots = request.data.get('unavailable_slots', [])
        for slot in unavailable_slots:
            CustomUnavailability.objects.create(
                screen=screen, date=slot['date'], start_time=slot['start'], end_time=slot['end']
            )

        # Save unavailable dates
        unavailable_dates = request.data.get('unavailable_dates', [])
        for date in unavailable_dates:
            CustomUnavailability.objects.create(screen=screen, date=date)

        return Response({'message': 'Custom unavailability added.'}, status=status.HTTP_200_OK)

class SlotView(APIView):
    def get(self, request, id):
        screen_id = request.query_params.get('screen_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        screen = Screen.objects.get(id=screen_id)

        # Fetch all slots in the date range
        slots = Slot.objects.filter(
            screen=screen,
            start_time__gte=start_date,
            end_time__lte=end_date,
            is_available=True
        )

        # Exclude slots that overlap with custom unavailability
        custom_unavailability = CustomUnavailability.objects.filter(screen=screen)
        for unavailable in custom_unavailability:
            slots = slots.exclude(
                start_time__lt=unavailable.end_time, end_time__gt=unavailable.start_time
            )

        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
