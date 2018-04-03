# _*_ encoding:utf-8 _*_
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from django.http import JsonResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restful.settings')

import django

django.setup()

from tempsensor.models import Sensor, TempValue


def get_location():
    location = []
    sensor = Sensor.objects.all()
    try:
        for s in sensor:
            location.append([s.x, s.y])
        return location
    except:
        raise ValueError


def get_temp_bytime():
    temp = []
    """
    当前仅包含一组工况，暂时提取全部
    目标根据时间查询工况，或距离查询时间最近工况
    """
    tempvalue = TempValue.objects.all()
    try:
        for t in tempvalue:
            temp.append(float(t.value))
        return temp
    except:
        raise ValueError


# 计算点与点之间距离
def cpt_distance(di, dj):
    dij = math.sqrt((di[0]-dj[0])**2+(di[1]-dj[1])**2)
    return dij


# 计算实测点半方差
def cpt_semi_variance(ci, cj):
    rij = ((ci-cj)**2)/2
    return rij


if __name__ == '__main__':
    loc = np.array(get_location())
    temp = np.array(get_temp_bytime())

    # distance = []
    # for l in loc:
    #     dij = map(cpt_distance, [l]*loc.__len__(), loc)
    #     distance.append(dij)
    # distance = np.array(distance)
    #
    # semivariance = []
    # for t in temp:
    #     rij = map(cpt_semi_variance, [t]*temp.__len__(), temp)
    #     semivariance.append(rij)
    # semivariance = np.array(semivariance)
    #
    # dis_list = distance.reshape((distance.size, 1))
    # var_list = semivariance.reshape((semivariance.size, 1))
    #
    # print dis_list
    # print var_list
    #
    # fig = plt.figure()
    # plt.scatter(dis_list, var_list)
    # plt.show()
    grid_x, grid_y = np.mgrid[0:21480:100j, 0:21480:100j]
    grid_z = griddata(loc, temp, (grid_x, grid_y), method='cubic')
    #
    # print grid_x
    # print grid_y
    # print grid_z

    # def func(x, y):
    #     return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2
    #
    #
    # grid_xx, grid_yy = np.mgrid[0:1:100j, 0:1:200j]
    #
    # points = np.random.rand(1000, 2)
    # values = func(points[:, 0], points[:, 1])
    #
    # grid_z2 = griddata(points, values, (grid_xx, grid_yy), method='cubic')
    #
    # print grid_z2
    # plt.imshow(grid_z.T, extent=(0, 21480, 0, 21480), origin='lower')
    #
    # print grid_z[0]
    # print grid_z
    #
    # plt.show()
    res = {}
    res['width'] = grid_z.shape[0]
    res['height'] = grid_z.shape[1]
    grid_z = np.nan_to_num(grid_z.T.reshape(grid_z.size, 1))

    res['values'] = grid_z.tolist()
    response = JsonResponse(res, safe=False)

    print response.content


