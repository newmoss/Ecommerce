# Generated by Django 4.2.1 on 2023-05-26 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_usuario_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('idSolicitud', models.AutoField(primary_key=True, serialize=False)),
                ('productoSolicitado', models.CharField(max_length=50)),
            ],
        ),
    ]
