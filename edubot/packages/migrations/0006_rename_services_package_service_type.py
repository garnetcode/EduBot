# Generated by Django 3.2.12 on 2023-02-07 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0005_package_services'),
    ]

    operations = [
        migrations.RenameField(
            model_name='package',
            old_name='services',
            new_name='service_type',
        ),
    ]
