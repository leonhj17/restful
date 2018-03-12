# _*_ encoding:utf-8 _*_
from rest_framework import serializers
# class Sensor(models.Model):
#     sensorKks = models.CharField(max_length=10, default="", null=False)
#     x = models.FloatField(max_length=6, default=-1.0)
#     y = models.FloatField(max_length=6, default=-1.0)
#     row = models.IntegerField(default=-1)
#     column = models.IntegerField(default=-1)
#
#     class Meta:
#         ordering = ("sensorKks",)


class SensorSerializer(serializers.Serializer):
    sensorKks = serializers.CharField(max_length=10)
    x = serializers.FloatField()
    y = serializers.FloatField()
    row = serializers.IntegerField()
    column = serializers.IntegerField()

1