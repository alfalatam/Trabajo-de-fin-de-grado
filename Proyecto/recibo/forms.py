from django import forms
from .models import Ticket
from datetime import datetime
import uuid

from django.utils.crypto import get_random_string


class TicketForm(forms.ModelForm):

    # unique_id = get_random_string(length=6)
    # titleFormat = datetime.today().strftime('%d/%m/%Y')+'-' + unique_id

    # title = forms.CharField(widget=forms.TextInput(
    #     attrs={'value': titleFormat}), required=True, max_length=30)

    class Meta:
        ''' Ticket form '''
        model = Ticket
        fields = ['title', 'payment', 'data']


class UserTicketForm(forms.ModelForm):
    class Meta:
        ''' Check '''
        model = Ticket
        fields = ['user']


class TicketModelForm(forms.ModelForm):
    class Meta:
        ''' Form to create and manage the tickets'''
        model = Ticket
        fields = [
            'title',
        ]
