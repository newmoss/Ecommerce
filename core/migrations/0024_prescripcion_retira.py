# Generated by Django 4.0.3 on 2022-06-20 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_retiro'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescripcion',
            name='retira',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]