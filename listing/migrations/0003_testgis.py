# Generated by Django 5.1.4 on 2025-01-12 15:33

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0002_propertyamenity_propertyfeature_propertytype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestGis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('address', models.CharField(default='', max_length=255)),
            ],
        ),
    ]