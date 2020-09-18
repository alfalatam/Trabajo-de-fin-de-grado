from django.shortcuts import render, redirect
from .forms import RegisterCustomerForm, RegisterStoreForm

# Create your views here.


def register(response):
    if(response.method == "POST"):
        form = RegisterCustomerForm(response.POST)
        if(form.is_valid()):
            form.save()
            return redirect("/inicio")
        else:
            return render(response, "register/register.html", {'form': form})

    else:
        form = RegisterCustomerForm()
    return render(response, "register/register.html", {"form": form})


def home(request):

    return render(request, "home.html")


def selectRegister(request):

    return render(request, "register/selectRegister.html")


def recibos(response):
    return render(response, "recibos.html", {})


def registerStore(response):
    if(response.method == "POST"):
        form = RegisterStoreForm(response.POST)
        if (form.is_valid()):
            form.save()
            return redirect("/inicio")
        else:
            return render(response, "register/registerStore.html", {'form': form})

    else:
        form = RegisterStoreForm()
    return render(response, "register/registerStore.html", {"form": form})
