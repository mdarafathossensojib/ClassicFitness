from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager
from cloudinary.models import CloudinaryField

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = CloudinaryField('profileImage', blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email