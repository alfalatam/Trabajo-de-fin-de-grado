from django.db import models
# from recibo.models import Ticket
from register.models import Store
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.db.models import DateField
from datetime import datetime
# from django.urls import reverse
# from django.shortcuts import redirect

# Create your models here.


class Producto(models.Model):
    # Relaciones
    # ticket = models.ForeignKey(
    #     Ticket, on_delete=models.CASCADE, null=False, blank=False)
    # Relacion con user(Store)
    store = models.ForeignKey(
        Store, on_delete=models.DO_NOTHING, null=False, blank=False)

    # Atributos
    name = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1,
                                   validators=[MaxValueValidator(999), MinValueValidator(1)])
    price = models.DecimalField(
        decimal_places=2, max_digits=10, default='00.00')

    warranty = models.IntegerField(default=0, blank=True)

    momentOfCreation = models.DateTimeField(auto_now_add=datetime.now)

    def actualizaPrecioTicket(self):
        priceToAdd = self.price
        self.ticket.price += priceToAdd

        t = self.ticket
        t.price += priceToAdd

        # warranty = models.CharField()
    def save(self, **kwargs):
        super(Producto, self).save(**kwargs)
        store = Store.objects.get(pk=self.store.user.id)
        store.save()

    def __str__(self):
        '''Returns the name of the ticket'''
        return self.name
