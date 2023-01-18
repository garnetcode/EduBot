# Generated by Django 4.1.5 on 2023-01-11 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0002_payment_package"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="payment_type",
            field=models.CharField(
                choices=[("1", "PayPay"), ("2", "PayNow")], default="1", max_length=255
            ),
        ),
    ]
