# _*_ encoding:utf-8 _*_
import xadmin
from .models import Sensor, TempValue, TempCenter


# @xadmin.site.register(Sensor)
class SensorAdmin(object):
    list_display = ("sensorKks", "x", "y", "row", "column")
    search_fields = ["sensorKks", "row", "column"]
    list_filter = ["sensorKks", "row", "column"]


class TempValueAdmin(object):
    list_display = ("sensorKks", "value", "time")
    search_fields = ["sensorKks"]
    list_filter = ['sensorKks', "time"]


class TempCenterAdmin(object):
    list_display = ('center_x', 'center_y', 'distance', 'angle', 'region', 'time')
    search_fields = ['region']
    list_filter = [ 'distance', 'angle', 'region', 'time']

xadmin.sites.site.register(Sensor, SensorAdmin)
xadmin.sites.site.register(TempValue, TempValueAdmin)
xadmin.sites.site.register(TempCenter, TempCenterAdmin)
