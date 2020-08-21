from django.shortcuts import render, redirect
from .forms import RegisterForm, RegisterStoreForm

# Create your views here.


def register(response):
    if(response.method == "POST"):
        form = RegisterForm(response.POST)
        if(form.is_valid()):
            form.save()
            return redirect("/inicio")
        else:
            return render(response, "register/register.html", {'form': form})

    else:
        form = RegisterForm()
    return render(response, "register/register.html", {"form": form})


def home(request):

    return render(request, "home.html")


def recibos(response):
    return render(response, "recibos.html", {})


def registerStore(response):
    if(response.method == "POST"):
        form = RegisterStoreForm(response.POST)
        if(form.is_valid()):
            form.save()
            return redirect("/inicio")
        else:
            return render(response, "register/registerStore.html", {'form': form})

    else:
        form = RegisterForm()
    return render(response, "register/registerStore.html", {"form": form})
