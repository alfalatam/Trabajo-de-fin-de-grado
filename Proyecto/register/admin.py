from django.contrib import admin
from register.forms import RegisterForm
from tickets.models import Ticket
from productos.models import Producto
# from .models import UserProfile
# Register your models here.

admin.site.register(Ticket)

admin.site.register(Producto)

# class RegisterAdmin(admin.ModelAdmin):
#     list_display = ("email", "name", "telefono")
#     search_fields = ("name", "lastName" "email")


# admin.site.register(RegisterForm, RegisterAdmin)
# admin.site.register(UserProfile)
