from rest_framework import serializers
from services.models import GymService, GymGallery, Feedback
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


class FeedbackSerializer(serializers.ModelSerializer):
    member_email = serializers.EmailField(source='member.email', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'member', 'member_email', 'fitness_class', 'rating', 'comment', 'created_at']
        read_only_fields = ['member', 'member_email',  'fitness_class', 'created_at']

    # def create(self, validated_data):
    #     request = self.context['request']
    #     class_id = self.context['class_id']
    #     fitness_class = get_object_or_404(FitnessClass, pk=class_id)

    #     validated_data['member'] = request.user
    #     validated_data['fitness_class'] = fitness_class

    #     return super().create(validated_data)

