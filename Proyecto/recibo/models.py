from django.db import models
from datetime import datetime
from annoying.fields import AutoOneToOneField
from register.models import User, Customer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import DateField
from datetime import date
# Create your models here.
import uuid


class Ticket(models.Model):
    # Relaciones
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ticketList", null=True, blank=False)

    # Atributos
    title = models.CharField(
        max_length=35, default=datetime.today().strftime('%d/%m/%Y')+'-'+uuid.uuid4().hex[:6].upper())
    empresa = models.CharField(max_length=20, default='Nombre de la empresa')

    address = models.CharField(max_length=50, default='')
    identifier = models.CharField(unique=True,
                                  max_length=30, default='autogenerateduniqueid-custom')

    price = models.DecimalField(
        decimal_places=2, max_digits=10, default='00.00')

    momentOfCreation = models.DateTimeField(
        auto_now_add=datetime.now)

    # companyIdentifier = models.CharField(max_length=11, default='0')
    # barcode = models.DateField()
    # paymentMethod = models.CharField()
    data = models.TextField(blank=True, null=True)

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


# TODO MIRAR BIEN ESTO
class ScannedTicket(models.Model):
        # Relaciones
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="scannedTicketList", null=True, blank=False)

    title = models.CharField(
        max_length=35, default=datetime.today().strftime('%d/%m/%Y'))

    empresa = models.CharField(max_length=20, default='Nombre de la empresa')

    photo = models.ImageField(upload_to='user_scannedTickets')

    def __str__(self):
        return self.title


class TicketLink(models.Model):

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="ticketLink", null=True, blank=False)

    url = models.CharField(max_length=150, blank=False, null=False)
    is_shared = models.BooleanField(default=False)

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
