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
from Proyecto.views import inicio, profile
from register import views as v
from register.views import home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from recibo import views
from pdf import views as viewsPdf
from usuarios import views as viewsUsers
from producto import views as viewsProduct


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio),
    path('selectRegister/', v.selectRegister, name="register"),
    path('register/', v.register, name="register"),
    path('registerStore/', v.registerStore, name="registerStore"),
    path('home/', home, name="home"),
    path('', include("django.contrib.auth.urls")),
    path('recibos/', v.recibos, name="recibos"),
    # path('render/pdf/', viewsPdf.gen_pdf, name='pdf'),
    # path('pdf/', viewsPdf.pdfGenerator, name="pdf"),
    path("misRecibos/", views.misRecibos, name="misRecib"),  # <-- added
    path("Notificationes/", viewsProduct.misNotificaciones,
         name="misNotificaciones"),  # <-- added
    path("recibo", views.recibo, name="recibo"),
    path("resultadosBusqueda/", views.busqueda_recibos, name="recibosBusq"),
    path("buscar/", views.buscar),
    path('generate-pdf', viewsPdf.generate_pdf, name='generate-pdf'),
    path('profile/', profile),
    path('importScanned/', views.scannedTiket),


    # beta
    path('delete/', viewsUsers.delete_user, name='delete'),






]
