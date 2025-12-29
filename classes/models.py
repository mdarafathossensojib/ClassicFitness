from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class FitnessClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='classes/',
        blank=True,
        null=True
    )
    instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='instructed_classes'
    )
    class_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ClassBooking(models.Model):
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'MEMBER'}
    )
    fitness_class = models.ForeignKey(
        FitnessClass,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booked_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('member', 'fitness_class')

    def __str__(self):
        return f"{self.member} -> {self.fitness_class}"
