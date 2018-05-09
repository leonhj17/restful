# _*_ encoding:utf-8 _*_
from .models import Sensor, TempValue
from .serializers import SensorSerializer, TempValueSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
import numpy as np
from scipy.interpolate import griddata
from pandas import DataFrame as df
from random import random, seed
from datetime import datetime, timedelta

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
        # 查询并返回出最近时刻的烟温值
        time = TempValue.objects.values('time').order_by('time').last()
        value = TempValue.objects.filter(time__gt=time['time']-timedelta(seconds=1))
        # value = TempValue.objects.all()
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


# 测试 计算火焰中心
# 待写入异步任务
def get_center():
    # time
    obj = TempValue.objects.all()
    serializer = TempValueSerializer(obj, many=True)
    data = serializer.data
    x = np.array([])
    y = np.array([])
    value = np.array([])
    for dic in data:
        x = np.append(x, dic['sensorKks']['x'])
        y = np.append(y, dic['sensorKks']['y'])
        value = np.append(value, dic['value'])
    x_avg = np.dot(x, value.T)/value.sum()
    y_avg = np.dot(y, value.T)/value.sum()
    return [x_avg, y_avg]


# 测试 生成烟温数据
# 待写入异步任务
def simulate_gastemp():
    obj = Sensor.objects.all()
    serializer = SensorSerializer(obj, many=True)
    data = serializer.data

    def type_sin(param):
        seed()
        return 1 + np.sin(param / 21480 * np.pi) * 0.3 * ((1 - 2 * random()) / 10 + 1)

    data_df = df(data, columns=['sensorKks', 'x', 'y', 'value', 'time'])
    data_df['value'] = type_sin(data_df['x'])*type_sin(data_df['y'])*700
    data_df['time'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    data_df.to_csv('gastemp.csv', index=False, header=False, columns=['sensorKks', 'value', 'time'])
