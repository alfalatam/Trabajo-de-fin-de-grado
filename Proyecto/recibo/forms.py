from django import forms
from .models import ScannedTicket, Ticket


class ScannedTicketForm(forms.ModelForm):

    class Meta:
        ''' Delete'''
        model = ScannedTicket
        fields = ['user', 'title', 'empresa', 'photo']


class TicketForm(forms.ModelForm):
    class Meta:
        ''' Ticket form '''
        model = Ticket
        fields = ['title',  'payment', 'data']


class UserTicketForm(forms.ModelForm):
    class Meta:
        ''' Check '''
        model = Ticket
        fields = ['user']
