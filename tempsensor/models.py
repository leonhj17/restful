from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Sensor(models.Model):
    sensorKks = models.CharField(max_length=10, default="", null=False)
    x = models.FloatField(max_length=6, default=-1.0)
    y = models.FloatField(max_length=6, default=-1.0)
    row = models.IntegerField(max_length=5, default=-1)
    column = models.IntegerField(max_length=5, default=-1)

    class Meta:
        ordering = ("sensorKks",)


class TempValue(models.Model):
    sensroKks = models.ForeignKey(Sensor)
