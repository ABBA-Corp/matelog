# Generated by Django 4.1 on 2023-02-07 14:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_rename_price_leads_price_first_tarif_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.PositiveIntegerField(blank=True, null=True, verbose_name='Distance')),
                ('date', models.DateField()),
                ('vehicle_runs', models.CharField(choices=[('1', 'Yes'), ('0', 'No')], max_length=255, verbose_name='Vehicle Runs')),
                ('ship_via_id', models.CharField(choices=[('1', '1'), ('2', '2')], max_length=255, verbose_name='Ship via id')),
                ('price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Price')),
                ('tarif', models.CharField(choices=[('+200', '+200'), ('+500', '+500')], max_length=255, verbose_name='Tarif')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('ship_type', models.CharField(choices=[('An individual', 'An individual'), ('General', 'General')], max_length=255, verbose_name='Ship type')),
                ('first_name', models.CharField(max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('ship_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ship_fromappl', to='main.city')),
                ('ship_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ship_to_appl', to='main.city')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.carsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='AplicationNbm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nbm', models.CharField(blank=True, max_length=10, null=True, validators=[main.models.is_numeric_validator], verbose_name='Nbm')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nbms', to='main.applications')),
            ],
        ),
    ]
