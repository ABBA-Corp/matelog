# Generated by Django 4.1 on 2023-01-29 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0009_staticinformation_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticinformation',
            name='nbm',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Номер телефона'),
        ),
    ]
