# Generated by Django 4.1 on 2023-02-05 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0014_remove_metatags_meta_tags_metatags_meta_deck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='meta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admins.metatags'),
        ),
    ]
