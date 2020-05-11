from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticket
from producto.models import Producto
# Create your views here.


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
