# Generated by Django 4.0.3 on 2022-06-17 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_medicamento_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caducar',
            fields=[
                ('idCad', models.AutoField(primary_key=True, serialize=False)),
                ('motivo', models.CharField(max_length=500)),
                ('medicamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.medicamento')),
            ],
        ),
    ]