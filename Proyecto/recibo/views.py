from django.core.mail import send_mail
from Proyecto import settings
from django.shortcuts import render
# from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticket, TicketLink
from producto.models import Producto
from datetime import date, timedelta, datetime, timezone
import datetime

# Create your views here.
# Decorators
from django.contrib.auth.decorators import login_required
import traceback
from django.shortcuts import redirect
import producto
from .forms import ScannedTicketForm, TicketForm
from register.models import User, Store
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from .resources import TicketResource
import uuid
import json
# def recibo(response):

#     ticket = Ticket.objects.get(id=3)

#     return render(response, "recibo.html", {"recibo": ticket})
@login_required
def recibo(request):

    try:
        idRecibo = ""
        fullURL = request.get_full_path()
        print('eL ID QUE LE ESTOY PASANDO ES: ', idRecibo)
        idRecib = fullURL.split("=")
        idRecibo = idRecib[1]

        print('la id  es : ', idRecibo)
        ticket = Ticket.objects.get(id=idRecibo)

        # context = {}
        tLink = TicketLink.objects.get(ticket=ticket)

        shareUrl = "http://"+request.META['HTTP_HOST'] + \
            "/generate-public-pdf?url="+tLink.url
        print(shareUrl)
        # print(tLnk)
        # context['urlLink'] = tLink.url

        return render(request, "recibo.html", {"recibo": ticket, "tLink": tLink, "shareUrl": shareUrl})

    except Exception as e:
        print('Has pasado por la exception, buena suerte')
        trace_back = traceback.format_exc()
        message = str(e) + " " + str(trace_back)
        print(message)
        return render(request, 'error.html')


# def reciboUser(request, recibo):

#     try:
#         ticket = Ticket.objects.get(id=recibo)
#         ticketLink = TicketLink.objects.get(ticket=ticket)
#         # ticketLink.is_shared

#         return render(request, "recibo.html", {"recibo": ticket})

#     except Exception as e:
#         print('Has pasado por la exception, buena suerte')
#         trace_back = traceback.format_exc()
#         message = str(e) + " " + str(trace_back)
#         print(message)
#         return render(request, 'error.html')


def misRecibos(response):

    now = datetime.datetime.now()

    year = now.year

    return render(response, "misRecibos.html", {'year': year})

    # inside views.py


def index(response, id):
    ls = Ticket.objects.get(id=id)

    if ls in response.user.ticketList.all():

        if response.method == "POST":
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False

                    item.save()

            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt) > 2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid")
        return render(response, "misRecibos.html", {"ls": ls})

    return render(response, "inicio.html", {})


def busqueda_recibos(request):

    return render(request, 'resultadosBusqueda.html')


def buscar(request):

    if(request.GET["prd"]):

        # mensaje = "Artículo buscado: %r" % request.GET["prd"]
        producto = request.GET["prd"]

        if(len(producto) > 30):
            mensaje = "El valor introducido es demasiado largo"

            return render(request, "resultadosBusqueda.html", {"recibos": recibos, "query": producto})

        else:

            recibosPersonales = Ticket.objects.filter(user=request.user)
            recibos = recibosPersonales.filter(
                title__icontains=producto) | Ticket.objects.filter(empresa__icontains=producto)

            return render(request, "resultadosBusqueda.html", {"recibos": recibos, "query": producto})
    elif(request.GET["prd"] == ''):

        print('El path contiene la palabra: '+request.path)

        producto = request.GET["prd"]

        recibosPersonales = Ticket.objects.filter(user=request.user)

        return render(request, "resultadosBusqueda.html", {"recibos": recibosPersonales, "query": producto})

    # if(request.GET["prd"] is None):

    #     recibosPersonales = Ticket.filter(user=request.user)

    #     return render(request, "resultadosBusqueda.html", {"recibos": recibosPersonales, "query": producto})

    else:
        print(request)
        mensaje = "No se ha encontrado ningún recibo con los criterios de búsqueda dados"
    return HttpResponse(mensaje)


def importeTotal(recibo):
    importe = []
    importeTotal = 0.0
    data = recibo.data

    if(data):
        jsonData = json.loads(data)
        importe += [((float(p["priceIVA"])*int(p["quantity"])))
                    for p in jsonData]

        for el in importe:
            importeTotal += el

    # Devuelvo el valor con solo dos decimales
    return str(round(importeTotal, 2))
    # productosRecibo = Producto.objects.filter(ticket=recibo)
    # for p in productosRecibo:
    #     importe += p.quantity*p.price


# def identificadorUnico():
#     cadena
#     rng1 = random.sample(range(0, 9), 2)
#     rng2 = rng_generator()
#     cadena += recibo.user.usernames[:2]+recibo.company[:2] + \
#         rng1 + "-"+datetime.today().strftime('%d%m%Y')+"-"+rng2

#     return cadena


# def rng_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))


def scannedTiket(request):

    form = ScannedTicketForm(request.POST or None)

    if(form.is_valid()):
        form.save()
        form = ScannedTicketForm

    context = {
        'form': form

    }

    return render(request, "importScanned.html", context)


def sendMail(request, dict):

    res = 0
    subject = "Notificación de garantía"
    msg = "Uno de sus productos está cerca de perder su garantía, le recomendamos que tenga esto en cuenta"
    # msg.attach_file('/images/weather_map.png')
    # customer = 'alfonsoalarcontamayo27@gmail.com'
    to = []
    print(dict)
    for i in dict.items():
        # to = i.key()
        to.append(i[0])
        dataList = i[1]
        productName = dataList[0]
        ticketTitle = dataList[1]
        subject = "Aviso de garantía sobre:  %s" % (productName)
        msg = "Uno de sus productos está cerca de perder su garantía, le recomendamos que tenga esto en cuenta,más concretamente sobre el recibo %s" % (
            ticketTitle)

        res = send_mail(
            subject, msg, settings.EMAIL_HOST_USER, to)
        to.clear()

    if(res == 1):
        msg = "Mail Sent"
    else:
        msg = "Mail could not sent or no mails to send"
    return HttpResponse(msg)


def productsToNotify(request):

    productos = Producto.objects.all()
    dictToSendMails = {}
    mensaje = 'No hay productos para mandar'
    # try:

    # recorro los tickets
    # recorro el campo JSON
    #  en ellos el producto tendrá una fecha y un warranty days
    # recorro el método con esa info
    for p in productos:
        fechaLimite = p.momentOfCreation + timedelta(days=p.warranty)
        delta = fechaLimite - (datetime.datetime.now(timezone.utc))
        if (delta.days < 30):
            dictToSendMails[p.ticket.user.email] = [p.name, p.ticket.title]
            # dictToSendMails.add(p.ticket.user.email,
            #                     p.name, p.ticket.title)

            mensaje = "Mensajes enviados"
    sendMail(request=request, dict=dictToSendMails)
    return HttpResponse(mensaje)

    # except Exception as e:
    #     trace_back = traceback.format_exc()
    #     message = str(e) + " " + str(trace_back)
    #     print('peto')
    #     return render(request, 'error.html')


def createRecibo(request):

    form = TicketForm(request.POST or None)

    if(form.is_valid()):
        form.save()
        form = TicketForm

    context = {
        'form': form

    }

    return render(request, "createRecibo.html", context)


class ReciboCreateView(CreateView):
    template_name = "createRecibo.html"
    form_class = TicketForm
    # queryset = Producto.objects.all()

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = User.objects.get(id=self.request.user.id)
        obj.identifier = uuid.uuid4().hex[:16].upper()
        store = Store.objects.get(user_id=self.request.user.id)
        obj.companyIdentifier = store.identifier

        # obj.companyIdentifier = store.company

        obj.address = store.address
        obj.company_name = store.company_name
        # obj.companyIdentifier = store.companyIdentifier

        obj.save()

        # __Aqui creamos el ticketUrl___
        url = uuid.uuid4().hex[:32].upper()
        ticketLink = TicketLink.objects.create(
            ticket=obj, url=url, is_shared=False)

        return HttpResponseRedirect('/misRecibos/')


# Export data form import-export
def export_recibo(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        recibo_resource = TicketResource()
        user = request.user
        # store = Store.objects.get(user=user.id)

        queryset = Ticket.objects.filter(user=user)
        dataset = TicketResource().export(queryset)

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
