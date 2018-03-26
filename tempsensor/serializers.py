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
    sensorKks = SensorSerializer()
    value = serializers.FloatField()
    time = serializers.DateTimeField()

    def create(self, validated_data):
        """
        :param validated_data: 
        :return: 
        """
        return TempValue.objects.create(**validated_data)
