"""Imports"""
import uuid
from django.db import models

from services.payment_service import ProcessPayment

def get_payment_reference():
    """Generate payment reference"""
    return f"R{uuid.uuid4().int}"



class Payment(models.Model):
    """Payment Model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="payments",
        null=True
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    package = models.ForeignKey(
        "packages.Package",
        on_delete=models.CASCADE,
        related_name="payments",
        null=True
    )
    payment_type = models.CharField(
        max_length=255,
        choices= (
            ('1', 'PayPal'),
            ('2', 'PayNow')
        ), default='1'
    )
    payment_status = models.CharField(
        max_length=255,
        choices= (
            ('Awaiting Delivery', 'Awaiting Delivery'),
            ('Paid', 'Paid'),
            ('Failed', 'Failed'),
            ('Cancelled', 'Cancelled'),
            ('Declined', 'Declined'),

        ), default='Failed'
    )
    reference = models.CharField(max_length=255, default=get_payment_reference)
    method = models.CharField(max_length=255, default="paypal")
    is_paid = models.BooleanField(default=False)



    def __str__(self):
        """Unicode representation of Payment."""
        return f"{self.user} - {self.course}"

    class Meta:
        """Meta definition for Payment."""

        verbose_name = "Payment"
        verbose_name_plural = "Payments"


    @classmethod
    def create_payment(cls, course, package, method, user, payment_type):
        """Create a payment"""
        print("Creating payment")
        payment = cls(
            course=course,
            package=package,
            method=method.lower(),
            amount=package.price,
            user=user,
            payment_type="1" if payment_type.lower() == "paypal" else "2"
        )
        payment.save()

        return payment

    @classmethod
    def send_payment_request(cls, payment_object, phone_number):
        """Get a payment"""
        payment = ProcessPayment(
            paying_phone_number=phone_number,
            amount=round(payment_object.amount, 2),
            method=payment_object.method,
            reference=payment_object.reference,
            authemail="cto@bow-space.com",
        )
        return payment.process()

class OutsourcingFees(models.Model):
    """Fees Model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=255,
        choices= (
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
            ('Failed', 'Failed'),
            ('Cancelled', 'Cancelled'),
            ('Declined', 'Declined'),

        ), default='Pending'
    )
    reference = models.CharField(max_length=255, default=get_payment_reference)
    method = models.CharField(max_length=255, default="paynow")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        """Unicode representation of Fees."""
        return f"{self.amount}"

    class Meta:
        """Meta definition for Fees."""

        verbose_name = "Oursourcing Fees"
        verbose_name_plural = "Oursourcing Fees"

    @classmethod
    def create_fee(cls, payment_object, amount, method):
        """Create a fee"""
        print("Creating fee")
        fee = cls(
            amount=amount,
            method=method.lower(),
            reference=payment_object.reference
        )
        fee.save()
        return fee

    @classmethod
    def send_payment_request(cls, fee_object, phone_number):
        """Get a payment"""
        return ProcessPayment(
            paying_phone_number=phone_number,
            amount=round(fee_object.amount, 2),
            method=fee_object.method,
            reference=fee_object.reference,
            authemail=""
        ).process()