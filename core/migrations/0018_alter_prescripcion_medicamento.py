# Generated by Django 4.0.3 on 2022-06-17 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_prescripcion_medicamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescripcion',
            name='medicamento',
            field=models.CharField(max_length=100),
        ),
    ]