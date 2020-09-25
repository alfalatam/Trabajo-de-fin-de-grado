from django.shortcuts import render
from .models import Producto
from recibo.models import Ticket
# Create your views here.
# For notifications
from django.db.models.signals import post_save
from notifications.signals import notify
import traceback
from django.shortcuts import redirect
from datetime import datetime
from register.models import Store
from .forms import ProductoModelForm

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
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
def checkWarranty():

    products = Producto.objects.all()
    currentDay = datetime.now()

    for p in products:
        if(p.warranty < 0):
            warrantyDays = p.warranty
            dateOfCreation = p.momentOfCreation
            limitDate = dateOfCreation + datetime.timedelta(days=warrantyDays)
            user = p.ticket.user

            if(limitDate - daysFromToday >= 10):

                generateNotification(user=user, producto=p)
                print('checkwarranty mandada')


def misNotificaciones(request):

    try:
        user = request.user
        notifications = user.notifications

        unreaded = user.notifications.unread()
        readed = user.notifications.read()
        generateNotification(request, user)
        return render(request, "notificaciones.html", {"unreaded": unreaded, "readed": readed})

    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e) + " " + str(trace_back)
        print(message)
        return render(request, 'error.html')


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
    Producto.objects.filter(id=pk).delete()

    productos = Producto.objects.all()

    context = {
        'productos': productos,
    }

    return render(request, template, context)
