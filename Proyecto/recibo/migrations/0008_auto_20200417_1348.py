# Generated by Django 3.0.4 on 2020-04-17 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibo', '0007_auto_20200417_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(default='04/17/2020', max_length=30),
        ),
    ]
