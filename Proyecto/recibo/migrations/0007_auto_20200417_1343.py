# Generated by Django 3.0.4 on 2020-04-17 11:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recibo', '0006_auto_20200417_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=45),
        ),
    ]