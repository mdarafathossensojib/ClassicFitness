from django.db import models
from django.conf import settings
from classes.models import FitnessClass
from cloudinary.models import CloudinaryField

User = settings.AUTH_USER_MODEL


class GymService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField('GymService')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class GymGallery(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('GymGallery')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    fitness_class = models.ForeignKey(
        FitnessClass,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'fitness_class')

    def __str__(self):
        return f"{self.member} - {self.rating}"
