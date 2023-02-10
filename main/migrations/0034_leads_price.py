# Generated by Django 4.1 on 2023-02-10 10:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_shortapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Price'),
        ),
    ]
