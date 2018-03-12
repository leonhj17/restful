from django.shortcuts import render
from .models import Sensor
from .serializers import SensorSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SensorList(APIView):
    """
    list all sensor
    """
    def get(self, request, format=None):
        sensor = Sensor.objects.all()
        serializer = SensorSerializer(sensor, many=True)
        return Response(serializer.data)
