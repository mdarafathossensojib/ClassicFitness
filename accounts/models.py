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
    date_of_birth = models.DateField(blank=True, null=True)

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer-not-to-say', 'Prefer not to say'),
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    height = models.PositiveIntegerField(blank=True, null=True)  # cm
    weight = models.PositiveIntegerField(blank=True, null=True)  # kg

    FITNESS_GOAL_CHOICES = (
        ('lose-weight', 'Lose Weight'),
        ('build-muscle', 'Build Muscle'),
        ('improve-fitness', 'Improve Fitness'),
        ('flexibility', 'Flexibility'),
    )
    fitness_goal = models.CharField(
        max_length=30,
        choices=FITNESS_GOAL_CHOICES,
        blank=True,
        null=True
    )

    emergency_contact = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email