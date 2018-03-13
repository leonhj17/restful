# _*_ encoding:utf-8 _*_
from django.conf.urls import url
from tempsensor import views


urlpatterns = [
    url(r'^sensor/$', views.SensorList.as_view(), name='sensor'),
    url(r'^tempvalue/$', views.TempValueList.as_view(), name='tempvalue')
]