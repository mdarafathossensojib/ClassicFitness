from django.db import models
from django.conf import settings
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


