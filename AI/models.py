from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class AIPlan(models.Model):
    PLAN_TYPES = (
        ('workout', 'Workout Plan'),
        ('meal', 'Meal Plan'),
        ('health', 'Health Analytics'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_plans')
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    input_data = models.JSONField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan_type}"