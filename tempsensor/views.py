# _*_ encoding:utf-8 _*_
from .models import Sensor, TempValue
from .serializers import SensorSerializer, TempValueSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
import numpy as np
from scipy.interpolate import griddata

from interpolate import get_location, get_temp_bytime


class SensorList(APIView):
    """
    list all sensor
    """
    def get(self, request, format=None):
        sensor = Sensor.objects.all()
        serializer = SensorSerializer(sensor, many=True)
        return Response(serializer.data)


class SensorDetail(APIView):
    def get_object(self, pk):
        try:
            object = Sensor.objects.get(pk=pk)
            return object
        except:
            raise Http404

    def get(self, request, pk, format=None):
        sensor = self.get_object(pk=pk)
        serializer = SensorSerializer(sensor)
        return Response(serializer.data)


class TempValueList(APIView):
    """
    list all Temp Value
    """
    def get(self, request, format=None):
        value = TempValue.objects.all()
        value_serializer = TempValueSerializer(value, many=True)
        return Response(value_serializer.data)

    def post(self, request, format=None):
        value_serializer = TempValueSerializer(data=request.data)
        if value_serializer.is_valid():
            value_serializer.save()
            return Response(value_serializer.data, status=status.HTTP_201_CREATED)
        return Response(value_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempValueDetail(APIView):

    def get(self, request, id, format=None):
        try:
            object = TempValue.objects.get(id=id)
            serializer = TempValueSerializer(object)
            return Response(serializer.data)
        except:
            raise Http404


# 测试view 获取测点烟温点插值结果
def get_json_tempvalue(request):
    loc = np.array(get_location())
    temp = np.array(get_temp_bytime())

    grid_x, grid_y = np.mgrid[0:21480:100j, 0:21480:100j]
    grid_z = griddata(loc, temp, (grid_x, grid_y), method='cubic')

    res = {}

    res['width'] = grid_z.shape[0]
    res['height'] = grid_z.shape[1]
    grid_z = np.nan_to_num(grid_z.T.reshape(grid_z.size, 1))

    res['values'] = grid_z.tolist()
    return JsonResponse(res, safe=False)

