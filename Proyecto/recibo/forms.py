from django import forms
from .models import ScannedTicket, Ticket


class ScannedTicketForm(forms.ModelForm):

    class Meta:
        model = ScannedTicket
        fields = ['user', 'title', 'empresa', 'photo']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title',  'payment']


class UserTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['user']
