# Generated by Django 4.1 on 2023-02-04 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_carsmodel_country_carsmodel_vehicle_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='states',
            name='code',
            field=models.CharField(default='TX', max_length=255, verbose_name='State code'),
            preserve_default=False,
        ),
    ]