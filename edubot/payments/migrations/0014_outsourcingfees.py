# Generated by Django 4.1.5 on 2023-01-15 10:56

from django.db import migrations, models
import payments.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0013_alter_payment_payment_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="OutsourcingFees",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Paid", "Paid"),
                            ("Failed", "Failed"),
                            ("Cancelled", "Cancelled"),
                            ("Declined", "Declined"),
                        ],
                        default="Pending",
                        max_length=255,
                    ),
                ),
                (
                    "reference",
                    models.CharField(
                        default=payments.models.get_payment_reference, max_length=255
                    ),
                ),
                ("method", models.CharField(default="paynow", max_length=255)),
                ("is_paid", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Oursourcing Fees",
                "verbose_name_plural": "Oursourcing Fees",
            },
        ),
    ]