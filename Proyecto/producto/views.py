from django.http import HttpResponse
from .models import Producto
from .resources import ProductoResource
from tablib import Dataset
# from django.shortcuts import render
# from .models import Producto
# from recibo.models import Ticket
# Create your views here.
# For notifications
# from django.db.models.signals import post_save
from notifications.signals import notify
import traceback
# from django.shortcuts import redirect
# from datetime import datetime
from register.models import Store
from .forms import ProductoModelForm
# from tablib import Dataset
from django.shortcuts import redirect


from django.views.generic import CreateView, DetailView, UpdateView
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect

# from celery.schedules import crontab
# from celery.task import periodic_task


# from myapp.models import MyModel

def generateNotification(request, user):

    try:
        # Here the code
        # notify.send(instance, verb='was saved')
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


# @periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="mon"))
# TODO CHECK
# def checkWarranty():

#     products = Producto.objects.all()
#     # currentDay = datetime.now()

#     for p in products:
#         if(p.warranty < 0):
#             warrantyDays = p.warranty
#             dateOfCreation = p.momentOfCreation
#             limitDate = dateOfCreation + datetime.timedelta(days=warrantyDays)
#             user = p.ticket.user

#             if(limitDate - daysFromToday >= 10):

#                 generateNotification(user=user, producto=p)
#                 print('checkwarranty mandada')


# def misNotificaciones(request):

#     try:
#         user = request.user
#         notifications = user.notifications

#         unreaded = user.notifications.unread()
#         readed = user.notifications.read()
#         generateNotification(request, user)
#         return render(request, "notificaciones.html", {"unreaded": unreaded, "readed": readed})

#     except Exception as e:
#         trace_back = traceback.format_exc()
#         message = str(e) + " " + str(trace_back)
#         print(message)
#         return render(request, 'error.html')


def misProductos(request):

    try:
        user = request.user
        # store = Store.objects.filter(user=user)
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
    # queryset = Producto.objects.all()

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
        # obj.store = Store.objects.get(user_id=self.request.user.id)
        obj.save()

        return HttpResponseRedirect('/misProductos/')
        # print(form.cleaned_data)
        # return super().form_valid(form)


# class ProductoDeleteView(DeleteView):
#     template_name = 'deleteProducto.html'

#     def get_object(self):
#         id_ = self.kwargs.get("id")
#         return get_object_or_404(Producto, id=id_)

#     def get_success_url(self):
#         return HttpResponseRedirect('/misProductos/')

def delete_producto(request, pk):

    template = 'misProductos.html'

    user = request.user
    store = Store.objects.get(user=user)
    # producto = Producto.objects.filter(id=pk)
    producto = Producto.objects.get(id=pk)

    storeProperty = producto.store
    # print(storeProperty)

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
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        # producto_resource = ProductoResource()

        user = request.user
        store = Store.objects.get(user=user.id)

        queryset = Producto.objects.filter(store=store)
        dataset = ProductoResource().export(queryset)

        # dataset = producto_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(
                dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(
                dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response

    return render(request, 'exportData.html')


# Import data form import-export
def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        producto_resource = ProductoResource()
        dataset = Dataset()
        new_productos = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(
                new_productos.read().decode('utf-8'), format='csv')
            result = producto_resource.import_data(dataset, dry_run=True)
        # elif file_format == 'XLS (Excel)':
        #     imported_data = dataset.load(
        #         new_productos.read().decode('utf-8'), format='xls')
        #     result = producto_resource.import_data(dataset, dry_run=True)
        elif file_format == 'JSON':
            imported_data = dataset.load(
                new_productos.read().decode('utf-8'), format='json')
            # Testing data import
            result = producto_resource.import_data(imported_data, dry_run=True)

        if not result.has_errors():
            # Import now
            new_productos.import_data(imported_data, dry_run=False)

    return render(request, 'importData.html')


# def simple_upload(request):
#     if request.method == 'POST':
#         producto_resource = ProductoResource()
#         dataset = Dataset()
#         new_productos = request.FILES['myfile']
#         imported_data = dataset.load(new_productos.read())
#         result = producto_resource.import_data(
#             dataset, dry_run=True)  # Test the data import

#         if not result.has_errors():
#             producto_resource.import_data(
#                 dataset, dry_run=False)  # Actually import now

#     return render(request, 'importData.html')


def simple_upload(request):
    if request.method == 'POST':
        producto_resource = ProductoResource()
        dataset = Dataset()
        new_productos = request.FILES['myfile']
        user = request.user
        store = Store.objects.get(user=user)
        id_store = store.user.id

        imported_data = dataset.load(new_productos.read(), format='xls')
        # print(imported_data)
        for data in imported_data:
            print(data[1])
            value = Producto(
                data[0],
                # Este valor (1) es el id de la store, la store no puede modificarlo
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6]


            )
            data[1] == id_store
            value.save()

        # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'importData.html')
