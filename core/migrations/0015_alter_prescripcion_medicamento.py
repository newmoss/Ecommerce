# Generated by Django 4.0.3 on 2022-06-17 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_caducar_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescripcion',
            name='medicamento',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]