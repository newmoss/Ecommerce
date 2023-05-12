# Generated by Django 4.2.1 on 2023-05-12 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_motivo_delete_caducar_delete_prescripcion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('idInventario', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('idTienda', models.AutoField(primary_key=True, serialize=False)),
                ('nombreTienda', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='producto',
            name='stock',
        ),
        migrations.CreateModel(
            name='Inventario_producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.IntegerField()),
                ('nombreTienda', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('inventarioId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.inventario')),
                ('productoId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
        ),
        migrations.AddField(
            model_name='inventario',
            name='idTienda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tienda'),
        ),
    ]