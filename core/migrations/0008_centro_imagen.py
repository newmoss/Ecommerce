# Generated by Django 3.2.3 on 2021-07-05 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_centro'),
    ]

    operations = [
        migrations.AddField(
            model_name='centro',
            name='imagen',
            field=models.ImageField(null=True, upload_to='Centro'),
        ),
    ]