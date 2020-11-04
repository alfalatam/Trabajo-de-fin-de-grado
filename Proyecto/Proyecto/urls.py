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
from producto import views as productoViews
from pdf import views as viewsPdf
from usuarios import views as viewsUsers
from producto import views as viewsProduct
from django.conf.urls import url
from .views import quienesSomos

app_name = 'proyecto'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio),
    path('selectRegister/', v.selectRegister, name="selectRegister"),
    path('register/', v.register, name="register"),
    path('registerStore/', v.registerStore, name="registerStore"),
    path('home/', home, name="home"),
    path('', include("django.contrib.auth.urls")),
    path('recibos/', v.recibos, name="recibos"),
    # path('render/pdf/', viewsPdf.gen_pdf, name='pdf'),
    # path('pdf/', viewsPdf.pdfGenerator, name="pdf"),
    path("misRecibos/", views.misRecibos, name="misRecib"),  # <-- added
    # path("Notificationes/", viewsProduct.misNotificaciones,
    #      name="misNotificaciones"),  # <-- added
    path("Notificationes/", views.productsToNotify,
         name="misNotificaciones"),  # <-- added
    path("recibo", views.recibo, name="recibo"),
    #     path("reciboUser", views.reciboUser, name="reciboUser"),
    path("resultadosBusqueda/", views.busqueda_recibos, name="recibosBusq"),
    path("buscar/", views.buscar),

    path('generate-pdf', viewsPdf.generate_pdf, name='generate-pdf'),

    path('qr_code/', include('qr_code.urls', namespace="qr_code")),


    url(r'^generate-public-pdf',
        viewsPdf.generate_public_pdf, name="generate-public-pdf"),

    #     url(r'^generate-pdf/(?P<random_url>[-\w]+)/$',
    #         viewsPdf.generate_pdf, name='generate-pdf'),

    path('profile/', profile),
    path('importScanned/', views.scannedTiket),
    path("misProductos/", productoViews.misProductos,
         name="misProductos"),  # <-- added
    path('create/', viewsProduct.ProductoCreateView.as_view(),
         name='producto-create'),
    path('updateProducto/<int:id>/', viewsProduct.ProductoUpdateView.as_view(),
         name='producto-update'),
    #     path('deleteProducto/<int:id>/', viewsProduct.ProductoDeleteView.as_view(),
    #          name='producto-delete'),
    url(r'^deleteProducto/(?P<pk>\d+)$',
        viewsProduct.delete_producto, name="delete-producto"),
    # path('display/<int:pk>/', viewsProduct.ProductoDetailView.as_view(),
    #      name='producto-detail'),
    path('displayProducto/<int:pk>/',
         viewsProduct.ProductoDetailView.as_view(), name='detail'),

    path("exportData/", productoViews.export_data,
         name="export-data"),  # <-- added

    path("exportRecibo/", views.export_recibo,
         name="export-recibo"),  # <-- added

    path("importData/", productoViews.simple_upload,
         name="import-data"),  # <-- added

    path('createRecibo/', views.ReciboCreateView.as_view(),
         name='create-recibo'),

    path('QuienesSomos/', quienesSomos,
         name='QuienesSomos'),


    url(r'^updateRecibo/(?P<pk>\d+)$',
        views.update_recibo, name="update-recibo"),

    url(r'^cvopen/', views.camera, name="cvopen"),



    # beta
    path('delete/', viewsUsers.delete_user, name='delete'),


]
