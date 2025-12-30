from django.db import models
from django.conf import settings
from classes.models import FitnessClass

User = settings.AUTH_USER_MODEL


class Attendance(models.Model):
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
       related_name='attendances'
    )
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='attendances')
    is_present = models.BooleanField(default=True)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'fitness_class')

    def __str__(self):
        return f"{self.member.email} - {self.fitness_class.title}"
