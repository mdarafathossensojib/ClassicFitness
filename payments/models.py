from django.db import models
from django.conf import settings
from memberships.models import Subscription

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_PAID = 'PAID'
    STATUS_FAILED = 'FAILED'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_FAILED, 'Failed'),
    )

    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'MEMBER'}
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount} - {self.status}"


class Transaction(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    gateway_name = models.CharField(max_length=50)  # Stripe / SSLCommerz
    transaction_id = models.CharField(max_length=100)
    raw_response = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
