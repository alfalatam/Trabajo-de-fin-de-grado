from django.shortcuts import render
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler
from recibo.views import productsToNotify
from django.contrib.auth.decorators import login_required


def inicio(request):
    return render(request, "inicio.html")


def quienesSomos(request):
    return render(request, "QuienesSomos.html")


@login_required
def profile(request):
    return render(request, "profile/profile.html")


# IMPORTANT
# In pre production deactivate this to open the system the first time
# SCHEDULING CODE
# Comentar desde aqui para las migrations
# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")


# @register_job(scheduler, "interval", hours=24, replace_existing=True)
# def send_mail_task():
#     productsToNotify()


# register_events(scheduler)
# scheduler.start()
