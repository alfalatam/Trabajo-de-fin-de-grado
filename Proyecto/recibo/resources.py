from import_export import resources
from .models import Ticket


class TicketResource(resources.ModelResource):

    class Meta:
        '''DOC STRING'''
        model = Ticket
