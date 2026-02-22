from rest_framework import serializers
from .models import Booking
from trains.models import Train


class BookingCreateSerializer(serializers.Serializer):
    train_id = serializers.IntegerField()
    seats = serializers.IntegerField(min_value=1)


class BookingSerializer(serializers.ModelSerializer):
    train_number = serializers.CharField(source="train.train_number")
    train_name = serializers.CharField(source="train.name")
    source = serializers.CharField(source="train.source")
    destination = serializers.CharField(source="train.destination")

    class Meta:
        model = Booking
        fields = [
            "id",
            "train_number",
            "train_name",
            "source",
            "destination",
            "seats_booked",
            "booked_at",
        ]