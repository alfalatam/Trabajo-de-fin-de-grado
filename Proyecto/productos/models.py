from django.db import models
from tickets.models import Ticket
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Producto(models.Model):
    # Relaciones
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=False, blank=False)

    # Atributos
    name = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1,
                                   validators=[MaxValueValidator(100), MinValueValidator(1)])
    price = models.DecimalField(
        decimal_places=2, max_digits=10, default='00.00')
    # warranty = models.CharField()

    def __str__(self):
        return self.name
