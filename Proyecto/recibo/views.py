import datetime
import json
import traceback
import uuid
from datetime import date, datetime, timedelta, timezone

import producto
# Create your views here.
# Decorators
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from producto.models import Producto
from Proyecto import settings
from register.models import Store, User

from .forms import ScannedTicketForm, TicketForm, UserTicketForm
from .models import Ticket, TicketLink
from .resources import TicketResource

# QR Decoder
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

from django.shortcuts import get_object_or_404

from django.contrib import messages

import re

# Celery
# from celery import shared_task
# from celery.task import periodic_task

# from Proyecto.celery import app
# from celery.decorators import task


# def recibo(response):

#     ticket = Ticket.objects.get(id=3)

#     return render(response, "recibo.html", {"recibo": ticket})
@login_required
def recibo(request):

    print('=====================================1=======================================0')

    try:
        idRecibo = ""
        fullURL = request.get_full_path()
        print('eL ID QUE LE ESTOY PASANDO ES: ', idRecibo)
        idRecib = fullURL.split("=")
        idRecibo = idRecib[1]

        try:
            codeGenerate = fullURL.split("%")
            code = codeGenerate[1]

        except IndexError:
            code = 0

        print('la id  es : ', idRecibo)
        ticket = Ticket.objects.get(id=idRecibo)

        # context = {}
        tLink = TicketLink.objects.get(ticket=ticket)

        #  recibo

        form = UserTicketForm(request.POST or None)

        if(form.is_valid()):
            form.save()
            form = UserTicketForm

        context = {
            'form': form

        }

        # if (code == 0):
        #     message = None
        tupleN = (None, 'Recibo añadido correctamente al cliente',
                  'Ese recibo ya existe', 'Error interno, inténtelo de nuevo más tarde')

        codeString = tupleN[int(code)]

        # print('EL code es------>', code)
        # if (code == 1):
        #     apex = 'Recibo añadido correctamente al cliente'
        # elif (code == 2):
        #     apex = 'Ese recibo ya existe'
        # elif (code == 3):
        #     apex = 'Error interno, inténtelo de nuevo más tarde'
        # elif (code == 0):
        #     apex = None
        # print('El apex es ------>', apex)
        # else:
        #     message = ''

        # -----------------

        print('---------------------c', codeString)
        print('---------------------l', code)
        print('---------------------', )

        shareUrl = "http://"+request.META['HTTP_HOST'] + \
            "/generate-public-pdf?url="+tLink.url
        print(shareUrl)
        # print(tLnk)
        # context['urlLink'] = tLink.url

        return render(request, "recibo.html", {"recibo": ticket, "tLink": tLink, "code": code, 'codeString': codeString, "shareUrl": shareUrl})

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

    now = datetime.now()

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

    if (data):
        try:

            jsonData = json.loads(data)
            importe += [((float(p["priceIVA"])*int(p["quantity"])))
                        for p in jsonData]

        except ValueError as e:
            pass

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


def sendMail(dict):

    res = 0
    subject = "Notificación de garantía"
    msg = "Uno de sus productos está cerca de perder su garantía, le recomendamos que tenga esto en cuenta"
    # msg.attach_file('/images/weather_map.png')
    # customer = 'alfonsoalarcontamayo27@gmail.com'
    to = []
    # print(dict)
    for i in dict.items():
        # to = i.key()
        to.append(i[0])
        dataList = i[1]
        productName = dataList[0]
        ticketTitle = dataList[1]
        warranty = dataList[2]
        subject = "Aviso de garantía sobre:  %s" % (productName)
        msg = "Como nos indicó, le recordamos que uno de sus productos está cerca de expirar su garantía \n \n Nombre del recibo : <b> %s </b> \n Producto: %s \n Fecha fin de garantía: %s \n \n Atentamente, el equipo de E-tick " % (
            ticketTitle, productName, warranty)

        res = send_mail(
            subject, msg, settings.EMAIL_HOST_USER, to)
        to.clear()

    if(res == 1):
        msg = "Mail Sent"
    else:
        msg = "Mail could not sent or no mails to send"
    return HttpResponse(msg)


# @task(name="mails")
# @periodic_task(run_every=crontab(minute=0, hour='*/12'))
def productsToNotify():
    print('Procediendo al envío de avisos de garantías...')

    # productos = Producto.objects.all()
    # queryset of recibos
    recibos = Ticket.objects.filter(warranty=True)
    dictToSendMails = {}
    mensaje = 'No hay notificationes para mandar'
    for r in recibos:

        try:
            jsonData = json.loads(r.data)
            for p in jsonData:
                email = r.user.email
                name = p['name']
                # if(p['warranty'] is Non):
                warranty = p['warranty']
                format_str = '%d%m%Y'
                datetime_obj = datetime.strptime(warranty, format_str)

                # Fecha del producto
                # print(datetime_obj.date())
                # fecha actual
                # print((datetime.now(timezone.utc).date()))

                diffDays = datetime_obj.date() - (datetime.now(timezone.utc).date())
                daysToExpire = diffDays.days
                # print(daysToExpire)
                # print('La resta entre las dos fechas es:')
                # print(resta.days)
                if (diffDays.days < 8 and diffDays.days > 6):
                    # print('debe avisar por correo')
                    dictToSendMails[email] = [
                        name, r.title, datetime_obj.date()]

        except ValueError as e:
            pass

    sendMail(dict=dictToSendMails)
    return HttpResponse(mensaje)


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


def update_recibo(request, pk):

    template = 'misRecibos.html'
    recibo = Ticket.objects.get(id=pk)

    # print('====================================================')
    # print(recibo)
    # print('====================================================')
    # print(recibo.warranty)

    # bol = not recibo.warranty()
    recibo.warranty = not recibo.warranty
    recibo.save()

    # productos = Producto.objects.all()

    context = {
        # 'productos': productos,
    }

    return render(request, template, context)


def camera(request):

    if request.method == 'GET':

        reciboID = request.GET.get('recibo')
        recibo = Ticket.objects.get(pk=reciboID)
        # recibos = Ticket.objects.all()
        print(recibo)

    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_PLAIN

    while True:
        _, frame = cap.read()

        mail = None

        decodedObjects = pyzbar.decode(frame)
        # print(decodedObjects.data)

        for obj in decodedObjects:
            # print("Data", obj.data)

            decodeData = obj.data
            d = decodeData.decode("utf-8")
            mail = d[7:]

            # m = re.findall(rb"'(.*?)'", decodeData, re.DOTALL)
            # print('El valor decodificado es -->', d[7:])

            if mail is not None:
                try:
                    user = User.objects.get(email=mail)
                    obj = Ticket.objects.get(pk=recibo.id)
                    obj.identifier = None
                    obj.identifier = recibo.identifier + '-c'

                    try:
                        existingTicket = Ticket.objects.get(
                            identifier=obj.identifier)
                    except Ticket.DoesNotExist:
                        existingTicket = None

                    if (existingTicket is None):
                        print('====================================')
                        print('Entra en el IF')

                        obj.user = None
                        obj.user = user
                        obj.pk = None
                        obj.save()

                        b = TicketLink(is_shared=True, ticket=obj, url='')
                        b.save()

                        print('Recibo creado satisfactoriamente.')
                        cv2.destroyAllWindows()

                        message = 'Recibo creado correctamente'
                        return HttpResponseRedirect('/recibo?='+reciboID+'=%1', {'message': message})

                    else:
                        print('====================================')
                        print('Entra en el ELSE')
                        print('Ese recibo ya existe')
                        message = 'Recibo creado correctamente'
                        cv2.destroyAllWindows()
                        # message = 'Ese recibo ya ha sido asignado, compruebe en sus recibos si ya existe.'
                        return HttpResponseRedirect('/recibo?=' + reciboID+'=%2', {'message': message})

                except ValueError as e:
                    print(
                        'Parece que hay un error la creacion del recibo intentelo de nuevo más tarde')
                    cv2.destroyAllWindows()
                    message = 'Parece que ha habido un error en la operación, inténtelo de nuevo.'
                    return HttpResponseRedirect('/recibo?='+reciboID+'=%3', {'message': message})

            # found: 1234

        cv2.imshow("Frame", frame)
        # print('El texto es:', cv2.putText)

        key = cv2.waitKey(1)
        if key == 27:
            break
