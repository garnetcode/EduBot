# Generated by Django 3.2.12 on 2023-02-07 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0006_rename_services_package_service_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='service_type',
            field=models.CharField(choices=[('Course Registration', 'Course Registration'), ('Assignment Outsourcing', 'Assignment Outsourcing')], default='1', max_length=255),
        ),
    ]
