from django.contrib import admin
from register.forms import RegisterForm

from .models import Ticket

# from productos.models import Producto
# from .models import UserProfile
# Register your models here.

admin.site.register(Ticket)

# admin.site.register(Producto)
