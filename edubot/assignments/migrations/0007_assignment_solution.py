# Generated by Django 3.2.12 on 2023-02-04 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0006_alter_assignment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='solution',
            field=models.FileField(blank=True, null=True, upload_to='solutions'),
        ),
    ]
