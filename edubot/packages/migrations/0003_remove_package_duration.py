# Generated by Django 4.1.5 on 2023-01-11 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("packages", "0002_package_access_permissions_package_duration_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="package",
            name="duration",
        ),
    ]
