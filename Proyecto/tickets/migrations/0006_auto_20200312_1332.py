# Generated by Django 3.0.2 on 2020-03-12 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_auto_20200312_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='empresa',
            field=models.CharField(default='Nombre de la empresa', max_length=20),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='identifier',
            field=models.CharField(default='autogenerateduniqueid-custom', max_length=30),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.DecimalField(decimal_places=2, default='00.00', max_digits=10),
        ),
    ]