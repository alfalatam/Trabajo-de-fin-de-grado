from django.contrib import admin
from .models import Producto

# Register your models here.


# admin.site.register(Producto)


class ProductoAdmin(admin.ModelAdmin):

    search_fields = ("name", "quantity", "price")
    list_display = ('name',)


admin.site.register(Producto, ProductoAdmin)
