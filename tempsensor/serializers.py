# _*_ encoding:utf-8 _*_
from rest_framework import serializers
from .models import TempValue, Sensor


class SensorSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    sensorKks = serializers.CharField(max_length=10)
    x = serializers.FloatField()
    y = serializers.FloatField()
    row = serializers.IntegerField()
    column = serializers.IntegerField()


class TempValueSerializer(serializers.Serializer):
    # id = serializers.PrimaryKeyRelatedField(read_only=True)
    sensorKks = SensorSerializer(required=False)
    value = serializers.FloatField()
    time = serializers.DateTimeField()

    def create(self, validated_data):
        """
        :param validated_data: 
        :return: 
        """
        return TempValue.objects.create(**validated_data)


# 序列化截面温度中心参数
class TempCenterSerializer(serializers.Serializer):
    center_x = serializers.FloatField()
    center_y = serializers.FloatField()
    distance = serializers.FloatField()
    angle = serializers.FloatField()
    region = serializers.CharField()
    time = serializers.DateTimeField()
