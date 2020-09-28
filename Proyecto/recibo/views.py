from django.core.mail import send_mail
from Proyecto import settings
from django.shortcuts import render
# from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticket
from producto.models import Producto
from datetime import date, timedelta, datetime, timezone
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

        return render(request, "recibo.html", {"recibo": ticket})

    except Exception as e:
        print('Has pasado por la exception, buena suerte')
        trace_back = traceback.format_exc()
        message = str(e) + " " + str(trace_back)
        print(message)
        return render(request, 'error.html')


def misRecibos(response):
    return render(response, "misRecibos.html", {})

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
    importe = 0
    # productosRecibo = Producto.objects.filter(ticket=recibo)
    # for p in productosRecibo:
    #     importe += p.quantity*p.price

    return importe


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
    for p in productos:
        fechaLimite = p.momentOfCreation + timedelta(days=p.warranty)
        delta = fechaLimite - (datetime.now(timezone.utc))
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
        store = Store.objects.get(user_id=self.request.user.id)
        obj.address = store.address
        obj.company_name = store.company_name
        # obj.companyIdentifier = store.companyIdentifier
        obj.save()

        return HttpResponseRedirect('/misProductos/')
