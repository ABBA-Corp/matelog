# Generated by Django 4.1 on 2023-02-04 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0011_alter_articlecategories_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='admins.services'),
        ),
    ]