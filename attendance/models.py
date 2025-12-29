from django.db import models
from django.conf import settings
from classes.models import FitnessClass

User = settings.AUTH_USER_MODEL


class Attendance(models.Model):
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'MEMBER'}
    )
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_attendances'
    )
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'fitness_class')

    def __str__(self):
        return f"{self.member} - {self.fitness_class}"
