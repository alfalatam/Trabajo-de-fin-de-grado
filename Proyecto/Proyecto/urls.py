
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
from Proyecto.views import inicio, profile
from register import views as v
from register.views import home
from django.urls import path, include
from recibo import views
from pdf import views as viewsPdf
from usuarios import views as viewsUsers
from producto import views as viewsProduct
from django.conf.urls import url
from .views import quienesSomos
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.decorators import login_required

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

    path("misRecibos/", views.misRecibos, name="misRecib"),  # <-- added
    path("Notificationes/", views.productsToNotify,
         name="misNotificaciones"),  # <-- added
    path("recibo", views.recibo, name="recibo"),
    path("resultadosBusqueda/", views.busqueda_recibos, name="recibosBusq"),
    path("buscar/", views.buscar),

    path('generate-pdf', login_required(viewsPdf.generate_pdf), name='generate-pdf'),

    path('qr_code/', include('qr_code.urls', namespace="qr_code")),

    url(r'^generate-public-pdf',
        viewsPdf.generate_public_pdf, name="generate-public-pdf"),
    path('profile/', profile),
    path("misProductos/", viewsProduct.misProductos,
         name="misProductos"),  # <-- added
    path('create/', login_required(viewsProduct.ProductoCreateView.as_view()),
         name='producto-create'),
    path('updateProducto/<int:id>/', login_required(viewsProduct.ProductoUpdateView.as_view()),
         name='producto-update'),
    path('updateRecibo/<int:id>/', login_required(views.ReciboUpdateView.as_view()),
         name='recibo-update'),
    url(r'^deleteProducto/(?P<pk>\d+)$',
        login_required(viewsProduct.delete_producto), name="delete-producto"),
    url(r'^deleteRecibo/(?P<pk>\d+)$',
        login_required(views.delete_recibo), name="delete-recibo"),
    # path('display/<int:pk>/', viewsProduct.ProductoDetailView.as_view(),
    #      name='producto-detail'),
    path('displayProducto/<int:pk>/',
         login_required(
             viewsProduct.ProductoDetailView.as_view()), name='detail'),

    path("exportData/", login_required(viewsProduct.export_data),
         name="export-data"),  # <-- added

    path("exportRecibo/", login_required(views.export_recibo),
         name="export-recibo"),  # <-- added

    path("importData/", viewsProduct.subida,
         name="import-data"),  # <-- added

    path('createRecibo/', login_required(views.ReciboCreateView.as_view()),
         name='create-recibo'),

    path('QuienesSomos/', quienesSomos,
         name='QuienesSomos'),

    url(r'^updateRecibo/(?P<pk>\d+)$',
        login_required(views.update_recibo), name="update-recibo"),

    url(r'^cvopen/', login_required(views.camera), name="cvopen"),

    # beta
    path('delete/', login_required(viewsUsers.delete_user), name='delete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
