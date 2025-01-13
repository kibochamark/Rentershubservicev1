# Generated by Django 5.1.4 on 2025-01-13 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0005_alter_property_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='garbage_charges',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='property',
            name='water_charges',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]