from rest_framework import serializers
from feedback.models import ClassFeedback, Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    member_email = serializers.EmailField(source='member.email', read_only=True)
    member_name = serializers.CharField(source='member.get_full_name', read_only=True) 
    member_photo = serializers.ImageField(source='member.profile_image', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'member', 'member_email', 'member_name', 'member_photo', 'rating', 'comment', 'created_at']
        read_only_fields = ['member', 'member_email', 'member_name', 'member_photo', 'created_at']


class ClassFeedbackSerializer(serializers.ModelSerializer):
    member_email = serializers.EmailField(source='member.email', read_only=True)

    class Meta:
        model = ClassFeedback
        fields = ['id', 'member', 'member_email', 'fitness_class', 'rating', 'comment', 'created_at']
        read_only_fields = ['member', 'member_email',  'fitness_class', 'created_at']