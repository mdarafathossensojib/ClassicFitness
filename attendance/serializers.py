from rest_framework import serializers
from attendance.models import Attendance
from memberships.models import Subscription
from django.contrib.auth import get_user_model

User = get_user_model()


class AttendanceSerializer(serializers.ModelSerializer):
    member_email = serializers.EmailField(source='member.email', read_only=True)
    class_title = serializers.CharField(source='fitness_class.title', read_only=True)
    member = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(subscription__is_active=True)
    )

    class Meta:
        model = Attendance
        fields = [
            'id',
            'fitness_class',
            'class_title',
            'member',
            'member_email',
            'is_present',
            'marked_at',
        ]
        read_only_fields = ['marked_at']
    
    def validate_member(self, member):
        if not Subscription.objects.filter(user=member, is_active=True).exists():
            raise serializers.ValidationError(
                "User does not have an active membership."
            )
        return member
