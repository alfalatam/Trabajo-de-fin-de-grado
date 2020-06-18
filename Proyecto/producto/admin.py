from django.contrib import admin
from .models import Producto

# Register your models here.


# admin.site.register(Producto)


class ProductoAdmin(admin.ModelAdmin):

    # Listado y buscador
    search_fields = ("name", "quantity", "price","warranty",)
    list_display = ('name',)


admin.site.register(Producto, ProductoAdmin)
