# Generated by Django 3.2.12 on 2023-02-06 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0007_assignment_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='grade',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
