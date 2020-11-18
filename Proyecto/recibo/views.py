import datetime
import json
import traceback
import uuid
from datetime import datetime, timezone

# import producto
# Create your views here.
# Decorators
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
# from producto.models import Producto
from Proyecto import settings
from register.models import Store, User

from .forms import TicketForm, UserTicketForm, TicketModelForm
from .models import Ticket, TicketLink
from .resources import TicketResource
from django.shortcuts import redirect, get_object_or_404

# QR Decoder
import cv2
# import numpy as np
import pyzbar.pyzbar as pyzbar

# from django.shortcuts import get_object_or_404

# from django.contrib import messages

# import re

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

    try:
        idRecibo = ""
        fullURL = request.get_full_path()
        idRecib = fullURL.split("=")
        idRecibo = idRecib[1]

        try:
            codeGenerate = fullURL.split("%")
            code = codeGenerate[1]

        except IndexError:
            code = 0

        ticket = Ticket.objects.get(id=idRecibo)

        price = importeTotal(ticket)

        # context = {}
        tLink = TicketLink.objects.get(ticket=ticket)

        #  recibo

        form = UserTicketForm(request.POST or None)

        if(form.is_valid()):
            form.save()
            form = UserTicketForm

        # context = {
        #     'form': form

        # }

        # if (code == 0):
        #     message = None
        tupleN = (None, 'Recibo añadido correctamente al cliente',
                  'Ese recibo ya existe', 'Error interno, inténtelo de nuevo más tarde', 'No se ha detectado ningún lector')

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

        # print('---------------------c', codeString)
        # print('---------------------l', code)
        # print('---------------------', )

        shareUrl = "http://"+request.META['HTTP_HOST'] + \
            "/generate-public-pdf?url="+tLink.url
        # print(shareUrl)
        # print(tLnk)
        # context['urlLink'] = tLink.url

        return render(request, "recibo.html", {"recibo": ticket, "tLink": tLink, "code": code, 'codeString': codeString, "shareUrl": shareUrl, "price": price})

    except Exception as e:
        # print('Has pasado por la exception, buena suerte')
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


def misRecibos(request):

    now = datetime.now()

    year = now.year

    user = request.user

    recibos = Ticket.objects.filter(user=user)

    for r in recibos:
        precio = r.dataPrice()
        print(precio)

    return render(request, "misRecibos.html", {'year': year, 'recibos': recibos})

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

            # return render(request, "resultadosBusqueda.html", {"recibos": recibos, "query": producto})
            return render(request, "resultadosBusqueda.html", {"query": producto})

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


def sendMail(dict):

    res = 0
    # Será el asunto del correo que se mande a cada uno de los usuarios
    subject = "Notificación de garantía"
    # Parte del cuerpo del mensaje, con un mensaje genérico
    msg = "Uno de sus productos está cerca de perder su garantía, le recomendamos que tenga esto en cuenta"

    to = []
    # Recorremos el diccionario del método productsToNotify
    for i in dict.items():
        # Seleccionados los valores del diccionario: emails, producto fechas...
        to.append(i[0])
        dataList = i[1]
        productName = dataList[0]
        ticketTitle = dataList[1]
        warranty = dataList[2]
        # Personalizamos el mensaje añadiendo información específica al correo
        subject = "Aviso de garantía sobre:  %s" % (productName)
        msg = "Como nos indicó, le recordamos que uno de sus productos está cerca de expirar su garantía \n \n Nombre del recibo :  %s  \n Producto: %s \n Fecha fin de garantía: %s \n \n Atentamente, el equipo de E-tick " % (
            ticketTitle, productName, warranty)

        # enviamos los correos
        res = send_mail(
            subject, msg, settings.EMAIL_HOST_USER, to)
        # vaciamos el listado de envios
        to.clear()

    # Avisamos si se ha realizado correctamte o si ha habido algún problema
    if(res == 1):
        msg = "Mail Sent"
    else:
        msg = "Mail could not sent or no mails to send"
    return HttpResponse(msg)


def productsToNotify():
    # Avisamos por consola el inicio del método de envío
    print('Procediendo al envío de avisos de garantías...')
    # Filtramos los recibos por aquellos los cuales se ha activado su seguimiento
    recibos = Ticket.objects.filter(warranty=True)
    # En este diccionario añadiremos la información para los mensajes
    dictToSendMails = {}
    # Si no hay ningún envío el sistema avisará con una notificación por consola
    mensaje = 'No hay notificationes para mandar'

    # Recorremos los envios
    for r in recibos:

        # Tratamos de cargar los datos en json de los productos por cada uno de los productos
        try:
            jsonData = json.loads(r.data)
            # Por cada producto seleccionamos la información requerida
            for p in jsonData:
                email = r.user.email
                name = p['name']
                # Seleccionamos la fecha y la convertimos a un formato fecha
                warranty = p['warranty']
                format_str = '%d%m%Y'
                datetime_obj = datetime.strptime(warranty, format_str)

                # Calculamos los dias de garantía restantes de los productos
                diffDays = datetime_obj.date() - (datetime.now(timezone.utc).date())
                if (diffDays.days < 8 and diffDays.days > 6):
                    dictToSendMails[email] = [
                        name, r.title, datetime_obj.date()]

        except ValueError as e:
            pass

    sendMail(dict=dictToSendMails)
    return HttpResponse(mensaje)


def createRecibo(request):

    form = TicketForm(request.POST or None)

    print(form)

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
        obj.companyIdentifier = store.logo
        obj.empresa = store.company_name

        obj.address = store.address
        obj.company_name = store.company_name

        obj.save()

        # __Aqui creamos el ticketUrl___
        url = uuid.uuid4().hex[:32].upper()
        ticketLink = TicketLink.objects.create(
            ticket=obj, url=url, is_shared=False)

        return HttpResponseRedirect('/misRecibos/')


# Exportamos los datos de la base de datos desde aqui
def export_recibo(request):
    if request.method == 'POST':
        # Añadimos varios formatos para dar opciones al usuario
        file_format = request.POST['file-format']
        user = request.user

        queryset = Ticket.objects.filter(user=user)
        dataset = TicketResource().export(queryset)

        # Formato CSV
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        # Formato JSON
        elif file_format == 'JSON':
            response = HttpResponse(
                dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        # Formato XLS(Excel)
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(
                dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response

    return render(request, 'exportData.html')


def update_recibo(request, pk):

    template = 'misRecibos.html'
    recibo = Ticket.objects.get(id=pk)

    recibo.warranty = not recibo.warranty
    recibo.save()

    context = {
        # 'productos': productos,
    }
    return redirect("/misRecibos")

    # return render(request, template, context)


def camera(request):

    # Comprobamos que es un GET
    if request.method == 'GET':

        # Accedemos a la información del recibo y a su ID
        reciboID = request.GET.get('recibo')
        recibo = Ticket.objects.get(pk=reciboID)

    # Accedemos a la cámara
    cap = cv2.VideoCapture(0)

    if (cap is None or not cap.isOpened()):
        print('Nothing detected')
        return HttpResponseRedirect('/recibo?='+reciboID+'=%4')

    # OPCIONAL: mostrar texto en cámara
    # font = cv2.FONT_HERSHEY_PLAIN

    while True:
        _, frame = cap.read()
        mail = None
        # decodificamos
        decodedObjects = pyzbar.decode(frame)
        # Recorremos los objetos
        for obj in decodedObjects:

            # Recorremos los objetos y decoficamos con uft-8
            decodeData = obj.data
            d = decodeData.decode("utf-8")

            # En algunos casos el email contiene http al generarse esto evita problemas en la lectura
            if (d.startswith('http')):
                mail = d[7:]
            else:
                mail = d

            # Realizamos una comprobación por si ya existe ese recibo
            exist = False
            if User.objects.filter(email=mail).exists():
                exist = True
            if (exist == False):
                # En caso de fallo cierra el lector y devuelve un error con la redirección
                cv2.destroyAllWindows()
                message = 'Parece que ha habido un error en la operación, inténtelo de nuevo.'
                return HttpResponseRedirect('/recibo?='+reciboID+'=%3', {'message': message})

            # Si todo va bien se genera y emite un aviso
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
                        obj.user = None
                        obj.user = user
                        obj.pk = None
                        obj.isCopy = True
                        obj.save()
                        b = TicketLink(is_shared=True, ticket=obj, url='')
                        b.save()
                        cv2.destroyAllWindows()

                        message = 'Recibo creado correctamente'
                        return HttpResponseRedirect('/recibo?='+reciboID+'=%1', {'message': message})

                    else:

                        message = 'Recibo creado correctamente'
                        cv2.destroyAllWindows()
                        return HttpResponseRedirect('/recibo?=' + reciboID+'=%2', {'message': message})

                # Si ocurre algún error inesperado, devuelve un aviso
                except ValueError as e:
                    print(
                        'Parece que hay un error la creacion del recibo intentelo de nuevo más tarde')
                    cv2.destroyAllWindows()
                    message = 'Parece que ha habido un error en la operación, inténtelo de nuevo.'
                    return HttpResponseRedirect('/recibo?='+reciboID+'=%3', {'message': message})

        cv2.imshow("Frame", frame)
        # Tecla ESC para cerrar manualmente el lector
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            return HttpResponseRedirect('/recibo?=' + reciboID)


def delete_recibo(request, pk):

    template = 'misRecibos.html'

    user = request.user
    user = User.objects.get(pk=user.pk)
    # producto = Producto.objects.filter(id=pk)
    recibo = Ticket.objects.get(id=pk)

    propertyUser = recibo.user

    if(propertyUser == user):
        recibo.delete()
        return redirect("/misRecibos")
    else:
        pass

    recibos = Ticket.objects.filter(user=user)

    context = {
        'recibos': recibos,
    }

    return render(request, 'misRecibos.html', context)


class ReciboUpdateView(UpdateView):
    template_name = 'createRecibo.html'
    form_class = TicketModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Ticket, id=id_)

    def form_valid(self, form):

        obj = form.save(commit=False)
        # obj.store = Store.objects.get(user_id=self.request.user.id)
        obj.save()

        return HttpResponseRedirect('/misRecibos/')
        # print(form.cleaned_data)
        # return super().form_valid(form)
