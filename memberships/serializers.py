from rest_framework import serializers
from memberships.models import MembershipPlan, Subscription


class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = ['id', 'name', 'price', 'duration_days', 'is_active']


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = MembershipPlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'start_date', 'end_date', 'is_active']

class MemberShipSerializer(serializers.Serializer):
    pass
