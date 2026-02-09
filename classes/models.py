from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

User = settings.AUTH_USER_MODEL



class Trainer(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = CloudinaryField('Trainer', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    experience = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    clients = models.IntegerField(default=0)
    specialties = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    philosophy = models.TextField(blank=True, null=True)
    schedule = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class FitnessClass(models.Model):
    title = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    longDescription = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    whatToExpect = models.TextField(blank=True, null=True)
    image = CloudinaryField('FitnessClass', blank=True, null=True)
    instructor = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        related_name='fitness_classes'
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
        related_name='class_bookings'
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
        return f"{self.member.email} -> {self.fitness_class.title}"
