from django.contrib import admin
from services.models import Feedback, GymGallery, GymService

# Register your models here.

admin.site.register(Feedback)
admin.site.register(GymGallery)
admin.site.register(GymService)