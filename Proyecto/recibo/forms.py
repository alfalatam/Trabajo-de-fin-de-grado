from django import forms
from .models import ScannedTicket


class ScannedTicketForm(forms.ModelForm):

    class Meta:
        model = ScannedTicket
        fields = ['user', 'title', 'empresa', 'photo']
