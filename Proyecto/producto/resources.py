from import_export import resources
from .models import Producto


class ProductoResource(resources.ModelResource):

    class Meta:
        '''Este método sirve como referencia para que django-export-import relacione bien el modelo'''
        model = Producto
