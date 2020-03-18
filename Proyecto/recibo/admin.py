from django.contrib import admin
from register.forms import RegisterForm

from .models import Tickets

admin.site.register(Tickets)

# admin.site.register(Producto)
