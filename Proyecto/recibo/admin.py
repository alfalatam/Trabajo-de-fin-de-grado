from django.contrib import admin
# from register.forms import RegisterCustomerForm

from .models import Ticket, ScannedTicket


# admin.site.register(Producto)

# TODO
class TicketAdmin(admin.ModelAdmin):

    search_fields = ("user__username", "title", "empresa", "identifier")
    list_display = ('user', 'title', 'empresa', 'identifier')


class ScannedTicketAdmin(admin.ModelAdmin):

    search_fields = ("user__username", "title")
    list_display = ('user', 'title')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(ScannedTicket, ScannedTicketAdmin)
