# Generated by Django 4.2.1 on 2023-05-12 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_rename_idtienda_inventario_tienda'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='inventario',
            field=models.CharField(default=2, max_length=20),
            preserve_default=False,
        ),
    ]