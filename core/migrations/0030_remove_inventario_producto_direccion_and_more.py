# Generated by Django 4.2.1 on 2023-05-12 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_inventario_inventario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario_producto',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='inventario_producto',
            name='nombreTienda',
        ),
    ]
