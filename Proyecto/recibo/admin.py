from django.contrib import admin
from register.forms import RegisterForm

from .models import Ticket


# admin.site.register(Producto)


class TicketAdmin(admin.ModelAdmin):

    search_fields = ("user__username", "title", "empresa", "identifier")
    list_display = ('user', 'title', 'empresa', 'identifier')


admin.site.register(Ticket, TicketAdmin)
