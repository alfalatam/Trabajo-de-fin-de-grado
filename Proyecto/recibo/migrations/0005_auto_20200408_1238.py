# Generated by Django 3.0.4 on 2020-04-08 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibo', '0004_ticket_companyidentifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='companyIdentifier',
            field=models.CharField(default='0', max_length=11),
        ),
    ]