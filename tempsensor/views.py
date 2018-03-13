from django.shortcuts import render
from .models import Sensor, TempValue
from .serializers import SensorSerializer, TempValueSerializer
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


class TempValueList(APIView):
    """
    list all Temp Value
    """
    def get(self, request, format=None):
        value = TempValue.objects.all()[:20]
        value_serializer = TempValueSerializer(value, many=True)
        return Response(value_serializer.data)

    def post(self, request, format=None):
        value_serializer = TempValueSerializer(data=request.data)
        if value_serializer.is_valid():
            value_serializer.save()
            return Response(value_serializer.data, status=status.HTTP_201_CREATED)
        return Response(value_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
