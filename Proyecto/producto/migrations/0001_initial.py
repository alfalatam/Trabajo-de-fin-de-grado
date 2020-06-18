# Generated by Django 3.0.4 on 2020-06-18 17:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recibo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('quantity', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(1)])),
                ('price', models.DecimalField(decimal_places=2, default='00.00', max_digits=10)),
                ('warranty', models.IntegerField(blank=True, default=0)),
                ('momentOfCreation', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recibo.Ticket')),
            ],
        ),
    ]
