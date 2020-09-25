from django import forms

from .models import Producto


class ProductoModelForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            # 'store',
            'name', 'quantity', 'price', 'warranty',
            # 'momentOfCreation',
        ]

        def __init__(self, *args, **kwargs):
            self.fields['store'].initial = 1
