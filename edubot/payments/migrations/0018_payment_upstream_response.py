# Generated by Django 3.2.12 on 2023-02-08 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0017_alter_payment_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='upstream_response',
            field=models.JSONField(default=dict),
        ),
    ]
