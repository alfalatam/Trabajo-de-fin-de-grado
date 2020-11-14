from django.http import HttpResponse
from .models import Producto
from .resources import ProductoResource
from tablib import Dataset
from notifications.signals import notify
import traceback
from register.models import Store
from .forms import ProductoModelForm
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect


def generateNotification(request, user):

    try:
        user2 = user
        description = 'Este es un aviso del sistema recordándole que la garantía del producto está por expirar'
        notify.send(user2, recipient=user2, verb='Aviso de garantía',
                    description=description)
        print('notificacion mandada')

    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e) + " " + str(trace_back)
        print(message)
        return render(request, 'error.html')


def misProductos(request):

    try:
        user = request.user
        store = Store.objects.get(user=user)
        productos = Producto.objects.filter(store=store)
        return render(request, "misProductos.html", {"productos": productos})

    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e) + " " + str(trace_back)
        print(message)
        return render(request, 'error.html')


class ProductoCreateView(CreateView):
    template_name = "createProducto.html"
    form_class = ProductoModelForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.store = Store.objects.get(user_id=self.request.user.id)
        obj.save()

        return HttpResponseRedirect('/misProductos/')


class ProductoDetailView(DetailView):

    def get(self, request, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=kwargs['pk'])
        context = {'producto': producto}
        return render(request, "displayProducto.html", context)


class ProductoUpdateView(UpdateView):
    template_name = 'createProducto.html'
    form_class = ProductoModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Producto, id=id_)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()

        return HttpResponseRedirect('/misProductos/')


def delete_producto(request, pk):

    template = 'misProductos.html'

    user = request.user
    store = Store.objects.get(user=user)
    producto = Producto.objects.get(id=pk)

    storeProperty = producto.store
    print(storeProperty)

    if(storeProperty == store):
        producto.delete()
        productos = Producto.objects.filter(store=store)

        return redirect("/misProductos")

    else:
        pass

    productos = Producto.objects.filter(store=store)

    context = {
        'productos': productos,
    }

    return render(request, template, context)


# Export data form import-export
def export_data(request):
    # POST
    if request.method == 'POST':
        # Get selected option from form
        formato = request.POST['file-format']

        user = request.user
        store = Store.objects.get(user=user.id)

        productos = Producto.objects.filter(store=store)
        newSet = ProductoResource().export(productos)

        # dataset = producto_resource.export()
        if formato == 'CSV':
            response = HttpResponse(newSet.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="productos.csv"'
            return response
        elif formato == 'JSON':
            response = HttpResponse(
                newSet.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="productos.json"'
            return response
        elif formato == 'XLS (Excel)':
            response = HttpResponse(
                newSet.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="productos.xls"'
            return response

    return render(request, 'exportData.html')


# Import data form import-export
def import_data(request):
    # POST
    # if request.method == 'POST':
    #     formato = request.POST['file-format']
    #     producto_resource = ProductoResource()
    #     dataset = Dataset()
    #     new_productos = request.FILES['importData']

    #     if formato == 'CSV':
    #         imported_data = dataset.load(
    #             new_productos.read().decode('utf-8'), format='csv')
    #         result = producto_resource.import_data(dataset, dry_run=True)

    #     elif formato == 'JSON':
    #         imported_data = dataset.load(
    #             new_productos.read().decode('utf-8'), format='json')
    #         result = producto_resource.import_data(imported_data, dry_run=True)
    #     if not result.has_errors():
    #         new_productos.import_data(imported_data, dry_run=False)

    return render(request, 'importData.html')


def subida(request):
    # POST
    if request.method == 'POST':
        newSet = Dataset()

        productos = request.FILES['myfile']

        # information about the user and the store
        user = request.user
        store = Store.objects.get(user=user)
        id_store = store.user.id
        #

        data = newSet.load(productos.read(), format='xls')
        for d in data:
            value = Producto(
                # El valor (1) es el id de la store, la store no puede modificarlo
                d[0], d[1], d[2], d[3], d[4], d[5], d[6]
            )
            data[1] == id_store
            # Save
            value.save()

    return render(request, 'importData.html')
