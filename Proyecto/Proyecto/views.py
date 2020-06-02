from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template import loader


# def inicio(request):
#     return HttpResponse("Pagina de inicio")


def inicio(request):
    return render(request, "inicio.html")


def profile(request):
    return render(request, "profile/profile.html")
