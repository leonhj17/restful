# _*_ encoding:utf-8 _*_
from .models import Sensor, TempValue, TempCenter
from .serializers import SensorSerializer, TempValueSerializer, TempCenterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse
from django.shortcuts import render
import numpy as np
import math
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
            object = TempValue.objects.filter(sensorKks_id=id)
            serializer = TempValueSerializer(object, many=True)
            return Response(serializer.data)
        except:
            raise Http404


# 测试view 获取假象温度中心点位置数据
# duration 提取数据时间段，从当前时刻往前
class TempCenterList(APIView):

    def get(self, request, duration='10', format=None):
        try:
            t = TempCenter.objects.values('time').order_by('time').last()
            endtime = t['time']
            if duration == '10':
                starttime = endtime - timedelta(minutes=10)
            else:
                starttime = endtime - timedelta(minutes=float(duration))
            obj = TempCenter.objects.filter(time__range=(starttime, endtime))
        except:
            raise Http404

        serializer = TempCenterSerializer(obj, many=True)
        return Response(serializer.data)

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
def get_center(time='last'):
    # time
    if time == 'last':
        t = TempValue.objects.values('time').order_by('time').last()
        obj = TempValue.objects.order_by('sensorKks').filter(time=t['time'])
    else:
        obj = TempValue.objects.order_by('sensorKks').filter(time=time)

    serializer = TempValueSerializer(obj, many=True)
    data = serializer.data

    loc = []
    temp = np.array([])
    for dic in data:
        loc.append([dic['sensorKks']['x'], dic['sensorKks']['y']])
        temp = np.append(temp, dic['value'])
    loc = np.array(loc)
    # print loc

    grid_x, grid_y = np.mgrid[0:21480:100j, 0:21480:100j]
    grid_z = griddata(loc, temp, (grid_x, grid_y), method='cubic')

    z = np.nan_to_num(grid_z.T)
    tx = grid_x.T * z
    ty = grid_y.T * z

    x_avg = tx.sum() / z.sum()
    y_avg = ty.sum() / z.sum()

    # x_avg = np.dot(x, value.T)/value.sum()
    # y_avg = np.dot(y, value.T)/value.sum()
    # return [x_avg, y_avg]
    center = np.array([10740, 10740])
    avg = np.array([x_avg, y_avg])
    tmp = (center-avg)**2
    # 偏心距
    r = np.sqrt(tmp.sum())

    def get_angle(avg, center):
        tmp = np.abs(avg-center)
        return math.degrees(math.atan(tmp[0]/tmp[1]))

    if x_avg > center[0] and y_avg < center[1]:
        angle = get_angle(avg, center)
        angle = float('%.2f' % angle)
        region = '1'
    elif x_avg > center[0] and y_avg > center[1]:
        angle =180 - get_angle(avg, center)
        angle = float('%.2f' % angle)
        region = '2'
    elif x_avg < center[0] and y_avg > center[1]:
        angle = 180 + get_angle(avg, center)
        angle = float('%.2f' % angle)
        region = '3'
    else:
        angle = 360 - get_angle(avg, center)
        angle = float('%.2f' % angle)
        region = '4'

    from tempsensor.models import TempCenter
    c = TempCenter(center_x=float('%.2f' % x_avg), center_y=float('%.2f' % y_avg), distance=float('%.2f' % r), angle=angle, region=region, time=obj[0].time)
    c.save()


# 测试 生成烟温数据
# 待写入异步任务
def simulate_gastemp():
    obj = Sensor.objects.all()
    serializer = SensorSerializer(obj, many=True)
    data = serializer.data

    def type_sin(param):
        seed()
        return 1 + (np.sin((param / 21480 - (1-2*random())/4) * np.pi)+1) * 0.15 * ((1 - 2 * random()) / 10 + 1)
        # return 1 + np.sin(param / 21480 * np.pi) * 0.3 * ((1 - 2 * random()) / 10 + 1)

    data_df = df(data, columns=['sensorKks', 'x', 'y', 'value', 'time'])
    data_df['value'] = type_sin(data_df['x'])*type_sin(data_df['y'])*700
    data_df['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data_df.to_csv('gastemp.csv', index=False, header=False, columns=['sensorKks', 'value', 'time'])


# 测试获取点击测点编号
def highcharats_get_kksid(request, id):
    print id
    return render(request, 'highcharts.html', {'id': id})
