from django.db import models
from datetime import datetime
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Ticket(models.Model):
    # Relaciones
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ticketList", null=False, blank=False)

    # Atributos
    title = models.CharField(max_length=30)
    empresa = models.CharField(max_length=20, default='Nombre de la empresa')
    identifier = models.CharField(
        max_length=30, default='autogenerateduniqueid-custom')
    price = models.DecimalField(
        decimal_places=2, max_digits=10, default='00.00')
    # date = models.CharField()
    companyIdentifier = models.CharField(max_length=11, default='000-000-000')
    # barcode = models.DateField()
    # paymentMethod = models.CharField()

    class paymentMethod(models.TextChoices):
        EFECTIVO = 'EF', ('Efectivo')
        TARJETA_DE_CREDITO = 'TC', ('Tarjeta de debito')
        TARJETA_DE_DEBITO = 'TD', ('Tarjeta de credito')

    payment = models.CharField(
        max_length=2,
        choices=paymentMethod.choices,
        default=paymentMethod.EFECTIVO,
    )

    def __str__(self):
        return self.title


# @receiver(post_save, sender=User)
# def create_ticket(sender, instance, created, **kwargs):
#     if created:
#         Ticket.objects.created(user=instance)


# @receiver(post_save, sender=User)
# def save_ticket(sender, instance, **kwargs):
#     instance.ticket.save()


# class product(models.Model):
#     name = models.CharField(max_length=30)
#     # quantity = models.CharField()
#     # price = models.CharField()
#     # warranty = models.CharField()

#     def __str__(self):
#         return self.name
