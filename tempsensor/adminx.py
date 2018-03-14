# _*_ encoding:utf-8 _*_
import xadmin
from .models import Sensor, TempValue


# @xadmin.site.register(Sensor)
class SensorAdmin(object):
    list_display = ("sensorKks", "x", "y", "row", "column")
    search_fields = ["sensorKks", "row", "column"]
    list_filter = ["sensorKks", "row", "column"]


class TempValueAdmin(object):
    list_display = ("sensorKks", "value", "time")
    search_fields = ["sensorKks"]
    list_filter = ["time"]

xadmin.sites.site.register(Sensor, SensorAdmin)
xadmin.sites.site.register(TempValue, TempValueAdmin)
