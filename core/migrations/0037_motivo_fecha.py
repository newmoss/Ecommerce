# Generated by Django 4.2.1 on 2023-05-27 22:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_inventario_producto_compartimiento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='motivo',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
    ]
