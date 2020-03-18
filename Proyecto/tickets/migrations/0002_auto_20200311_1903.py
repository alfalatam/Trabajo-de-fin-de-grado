# Generated by Django 3.0.2 on 2020-03-11 18:03

import annoying.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile2',
            fields=[
                ('user', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='product',
        ),
        migrations.DeleteModel(
            name='ticket',
        ),
    ]
