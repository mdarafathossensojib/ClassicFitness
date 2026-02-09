from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class MembershipPlan(models.Model):
    name = models.CharField(max_length=50)
    duration_days = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    yearlyPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    period = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True)
    features = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.plan}"
