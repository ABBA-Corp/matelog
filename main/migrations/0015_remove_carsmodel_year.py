# Generated by Django 4.1 on 2023-02-06 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_city_zip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carsmodel',
            name='year',
        ),
    ]