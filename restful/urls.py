"""restful URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^', include('snippets.urls')),
    url(r'^', include('tempsensor.urls', namespace='tempsensor')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'index/$', TemplateView.as_view(template_name='index.html')),
    url(r'contour/$', TemplateView.as_view(template_name='contour.html')),
    url(r'^siderbar/$', TemplateView.as_view(template_name='siderbar.html')),
    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
