from django import forms

from .models import Producto


class ProductoModelForm(forms.ModelForm):
    class Meta:
        ''' Form to create and manage the products'''
        model = Producto
        fields = [
            'name', 'quantity', 'price', 'warranty',
        ]
