# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime


# Create your models here.
@python_2_unicode_compatible
class Sensor(models.Model):
    sensorKks = models.CharField(max_length=10, default="", null=False)
    x = models.FloatField(max_length=6, default=-1.0)
    y = models.FloatField(max_length=6, default=-1.0)
    row = models.IntegerField(default=-1)
    column = models.IntegerField(default=-1)

    def __str__(self):
        return self.sensorKks

    class Meta:
        ordering = ("y", 'x')


class TempValue(models.Model):
    sensorKks = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.CharField(max_length=6, default=0)
    time = models.DateTimeField()

    def __str__(self):
        return self.value

    class Meta:
        ordering = ('time',)


class TempCenter(models.Model):
    center_x = models.FloatField(max_length=6, default=0, verbose_name='X中心')
    center_y = models.FloatField(max_length=6, default=0, verbose_name='Y中心')
    time = models.DateTimeField(null=False, default=datetime.now())

    class Meta:
        ordering = ('time',)
