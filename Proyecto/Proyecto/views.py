# from django.http import HttpResponse
# from django.shortcuts import render
# from django.template import Template, Context
# from django.template import loader
# Async tasks
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler
from recibo.views import productsToNotify

# def inicio(request):
#     return HttpResponse("Pagina de inicio")


def inicio(request):
    return render(request, "inicio.html")


def quienesSomos(request):
    return render(request, "QuienesSomos.html")


def profile(request):
    return render(request, "profile/profile.html")


# SCHEDULING CODE
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", hours=24, replace_existing=True)
def send_mail_task():
    productsToNotify()


register_events(scheduler)
scheduler.start()
