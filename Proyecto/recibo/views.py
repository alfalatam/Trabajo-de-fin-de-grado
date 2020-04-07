from django.shortcuts import render
from django.shortcuts import render
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
