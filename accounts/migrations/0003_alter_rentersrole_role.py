# Generated by Django 5.1.4 on 2025-01-02 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_rentersuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentersrole',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('LANDLORD', 'Landlord'), ('GROUNDAGENT', 'GroundAgent')], max_length=50, unique=True),
        ),
    ]
