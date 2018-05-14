from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Sensor, TempValue, TempCenter
from .serializers import SensorSerializer
import numpy as np
from random import random, seed
from pandas import DataFrame as df
from datetime import datetime
from csv_to_db import add_db, read_value_csv


@shared_task
def add(x, y):
    return x+y


@shared_task
def mul(x, y):
    return x*y


@shared_task
def interval_task():
    print 'interval task execute'


@shared_task
def crontab_task():
    print 'crontab task execute'


@shared_task
def simulate_gastemp():
    obj = Sensor.objects.all()
    serializer = SensorSerializer(obj, many=True)
    data = serializer.data

    def type_sin(param):
        seed()
        # 21480: boiler width
        return 1 + np.sin(param / 21480 * np.pi) * 0.3 * ((1 - 2 * random()) / 5 + 1)

    data_df = df(data, columns=['sensorKks', 'x', 'y', 'value', 'time'])
    data_df['value'] = type_sin(data_df['x'])*type_sin(data_df['y'])*700
    data_df['time'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    data_df.to_csv('gastemp.csv', index=False, header=False, columns=['sensorKks', 'value', 'time'])

    add_db(read_value_csv, TempValue, 'gastemp.csv')
