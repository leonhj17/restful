# _*_ encoding:utf-8 _*_
from django.conf.urls import url
# from .views import user_login
from django.contrib.auth import views as auth_views
from .views import validate_username, validate_username2


urlpatterns = [
    # url(r'login/$', user_login, name='login'),
    url(r'new_login/$', auth_views.login, {'template_name': 'login.html', 'redirect_field_name': 'page_home.html'}, name='new_login'),
    url(r'logout/$', auth_views.logout,  {'template_name': 'page_home.html'}, name='logout'),
    url(r'ajax/valid_username/$', validate_username2, name='validate_username'),
]
