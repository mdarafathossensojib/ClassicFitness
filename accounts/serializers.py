from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer
from rest_framework import serializers
from accounts.models import User, FreeTrialRequest

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserViewSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'phone_number', 'is_staff']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'profile_image', 'date_of_birth', 'gender', 'height', 'weight', 'fitness_goal', 'emergency_contact',
        ]



class FreeTrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeTrialRequest
        fields = "__all__"
        read_only_fields = ["created_at", "contacted"]

        
    def validate_email(self, value):
        if FreeTrialRequest.objects.filter(email=value).exists():
            raise serializers.ValidationError("You already requested a trial.")
        return value

