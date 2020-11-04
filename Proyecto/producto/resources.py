from import_export import resources
from .models import Producto


class ProductoResource(resources.ModelResource):

    class Meta:
        ''' Este método sirve como referencia para que django-export-import relacione bien el modelo'''
        model = Producto

    # def export(self, queryset=None, *args, **kwargs):
    #     # For example only export objects with ids in 1, 2, 3 and 4
    #     # user = kwargs.pop('user', None)
    #     # store = Store.objects.get(user=user.id)

    #     print('===================================================================')
    #     queryset = queryset and queryset.filter()
    #     queryset = Price.objects.exclude(...)
    #     data = ExportData().export(queryset)
    #     data.csv

    #     # print(queryset)
    #     return super(ProductoResource, self).export(queryset, *args, **kwargs)
