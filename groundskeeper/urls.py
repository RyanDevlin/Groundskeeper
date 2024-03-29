"""groundskeeper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from dashboard import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
import json
from django.conf import settings

with open(settings.BASE_DIR + "/config.json", "r") as file:
    data = json.load(file)
    admin_url = data["admin_url"]

urlpatterns = [
	url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
	path('', views.dash_index, name='dashboard'),
	path('dashboard/', include('dashboard.urls')),
	path(admin_url + '/', admin.site.urls),
]
