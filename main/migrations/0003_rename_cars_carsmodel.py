# Generated by Django 4.1 on 2023-02-04 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_cars_country'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cars',
            new_name='CarsModel',
        ),
    ]
