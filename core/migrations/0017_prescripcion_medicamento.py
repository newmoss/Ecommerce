# Generated by Django 4.0.3 on 2022-06-17 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_prescripcion_medicamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescripcion',
            name='medicamento',
            field=models.CharField(default='Some String', max_length=100),
        ),
    ]