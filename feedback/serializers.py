from rest_framework import serializers
from feedback.models import ClassFeedback, Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    member_email = serializers.EmailField(source='member.email', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'member', 'member_email', 'rating', 'comment', 'created_at']
        read_only_fields = ['member', 'member_email',  'created_at']


class ClassFeedbackSerializer(serializers.ModelSerializer):
    member_email = serializers.EmailField(source='member.email', read_only=True)

    class Meta:
        model = ClassFeedback
        fields = ['id', 'member', 'member_email', 'fitness_class', 'rating', 'comment', 'created_at']
        read_only_fields = ['member', 'member_email',  'fitness_class', 'created_at']