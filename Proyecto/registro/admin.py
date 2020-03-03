from django.contrib import admin
from registro import models
from registro.models import Registro

# Register your models here.


class RegistroAdmin(admin.ModelAdmin):
    # list_display('name')
    search_fields = ("name", "phone", "email")


admin.site.register(Registro, RegistroAdmin)
