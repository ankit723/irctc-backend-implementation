from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from trains.models import Train
from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer


class BookSeatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        train_id = serializer.validated_data["train_id"]
        seats_requested = serializer.validated_data["seats"]

        try:
            with transaction.atomic():

                # LOCK the train row
                train = Train.objects.select_for_update().get(id=train_id)

                if train.available_seats < seats_requested:
                    return Response(
                        {"error": "Not enough seats available"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Deduct seats
                train.available_seats -= seats_requested
                train.save()

                # Create booking
                booking = Booking.objects.create(
                    user=request.user,
                    train=train,
                    seats_booked=seats_requested
                )

            return Response({
                "message": "Booking confirmed",
                "booking_id": booking.id
            })

        except Train.DoesNotExist:
            return Response({"error": "Train not found"}, status=404)


class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).select_related("train")
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)