from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticket
from producto.models import Producto
from datetime import date
# Create your views here.
# Decorators
from django.contrib.auth.decorators import login_required
import traceback
from django.shortcuts import redirect


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
    productosRecibo = Producto.objects.filter(ticket=recibo)
    for p in productosRecibo:
        importe += p.quantity*p.price

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
