# Generated by Django 4.1 on 2023-02-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_leads_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='zip',
            field=models.CharField(max_length=255, unique=True, verbose_name='City zip'),
        ),
    ]