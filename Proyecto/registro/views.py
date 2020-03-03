from django.shortcuts import render

# Create your views here.


def inicio(request):
    # request.POST or None es una puerta OR se lee de izquierda a derecha , comprueba si se ha metido un valor y si no comprueba el None
    form = RegForm(request.POST or None)
    # Me muestra todas las funciones que puedo llamar de  form
    print(dir(form))

    if form.is_valid():

    return render(request, "inicio.html")


# def inicio(request):
#     form = RegForm(request.POST or None)

#     # Esta línea de abajo me permite conocer los comandos que puedo utilizar desde
#     # print(dir(form))

#     if form.is_valid():
#         form_data = form.cleaned_data
#         abc = form_data.get("email")
#         abc2 = form_data.get("nombre")
#         obj = Registrado.objects.create(email=abc, nombre=abc2)

#     context = {
#         "el_form": form,
#     }
#     return render(request, "inicio.html", context)
