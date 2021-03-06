"""Proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from Proyecto.views import inicio
from register import views as v
from register.views import home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from recibo import views
from pdf import views as viewsPdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio),
    path('register/', v.register, name="register"),
    path('home/', home, name="home"),
    path('', include("django.contrib.auth.urls")),
    path('recibos/', v.recibos, name="recibos"),
    # path('render/pdf/', viewsPdf.gen_pdf, name='pdf'),
    # path('pdf/', viewsPdf.pdfGenerator, name="pdf"),
    path("misRecibos/", views.misRecibos, name="misRecib"),  # <-- added



]
