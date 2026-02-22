from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import Train
from .serializers import TrainSerializer

import time
from rest_framework.permissions import IsAuthenticated
from analytics.mongo import search_logs_collection


class TrainCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = TrainSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_time = time.time()

        source = request.GET.get("source")
        destination = request.GET.get("destination")

        trains = Train.objects.filter(
            source__iexact=source,
            destination__iexact=destination
        )

        execution_time = (time.time() - start_time) * 1000

        # MongoDB logging
        log = {
            "user_id": request.user.id,
            "endpoint": "/api/trains/search/",
            "source": source,
            "destination": destination,
            "execution_time_ms": execution_time,
            "timestamp": time.time()
        }

        search_logs_collection.insert_one(log)

        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data)