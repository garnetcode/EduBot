# Generated by Django 4.1.5 on 2023-01-15 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assignments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pendingwork",
            name="deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]