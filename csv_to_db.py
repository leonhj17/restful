# _*_ encoding:utf-8 _*_
import os
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restful.settings')
import datetime
import pytz

import django

django.setup()

from tempsensor.models import Sensor, TempValue

sensor_path = os.path.join(os.getcwd(), 'sensor.csv')
temp_value_path = os.path.join(os.getcwd(), 'gastemp.csv')


# 将txt文件转化为列表形式，列表中每一项为字典
def read_sensor_csv(filepath):
    result = []
    with open(filepath, 'rb') as f:
        data = csv.reader(f)
        for line in data:
            cell = {}
            # 先找到对应外键，再插入数值
            cell['sensorKks'] = line[0]
            cell['x'] = float(line[1])
            cell['y'] = float(line[2])
            cell['row'] = float(line[3])
            cell['column'] = float(line[4])
            result.append(cell)
    return result


def read_value_csv(filepath):
    result = []
    with open(filepath, 'rb') as f:
        data = csv.reader(f)
        for line in data:
            cell = {}
            # 先找到对应外键，再插入数值
            cell['sensorKks'] = Sensor.objects.get(sensorKks=line[0])
            cell['value'] = float('%.1f' % float(line[1]))
            cell['time'] = datetime.datetime.strptime(
                line[2], '%Y/%m/%d %H:%M:%S'
            )
            result.append(cell)
    return result


# 批量导入
def add_db(func, model, filepath):
    kkslist = []
    data = func(filepath)
    for dic in data:
        kkslist.append(model(**dic))
    model.objects.bulk_create(kkslist)


if __name__ == '__main__':
    add_db(read_value_csv, TempValue, temp_value_path)
    print 'done'
