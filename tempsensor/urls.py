# _*_ encoding:utf-8 _*_
from django.conf.urls import url
from tempsensor import views
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^sensor/$', views.SensorList.as_view(), name='sensor'),
    url(r'^tempvalue/$', views.TempValueList.as_view(), name='tempvalue'),
    url(r'^sensor/(?P<pk>[0-9]+)/$', views.SensorDetail.as_view(), name='sensordetail'),
    url(r'tempvalue/(?P<id>[0-9]+)/$', views.TempValueDetail.as_view(), name='tempvaluedetail'),
    url(r'track/$', TemplateView.as_view(template_name='page_track.html'), name='track'),
    url(r'contour/$', TemplateView.as_view(template_name='page_contour.html'), name='contour'),
    url(r'home/$', TemplateView.as_view(template_name='page_home.html'), name='home'),
    url(r'get_json_tempvalue/$', views.get_json_tempvalue, name='get_json_tempvalue'),
    url(r'^tempcenter/(?P<duration>[0-9]+)/$', views.TempCenterList.as_view(), name='tempcenterlist'),
    url(r'^highcharts/(?P<id>[0-9]+)/$', views.highcharats_get_kksid)
]