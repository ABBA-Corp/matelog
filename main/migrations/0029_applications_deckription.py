# Generated by Django 4.1 on 2023-02-08 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_applications_adres'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='deckription',
            field=models.TextField(default='ssssd', verbose_name='Deskription'),
            preserve_default=False,
        ),
    ]