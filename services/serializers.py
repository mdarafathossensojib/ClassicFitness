from rest_framework import serializers
from services.models import GymService, GymGallery
from django.conf import settings
User = settings.AUTH_USER_MODEL


class GymServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymService
        fields = ['id', 'name', 'description', 'image', 'is_active', 'created_at']
        read_only_fields = ['created_at']

class GymGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GymGallery
        fields = ['id', 'title', 'image', 'uploaded_at']
        read_only_fields = ['uploaded_at']



