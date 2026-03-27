from django_filters.rest_framework import FilterSet
from memberships.models import MembershipPlan

class MembershipPlanFilter(FilterSet):
    class Meta:
        model = MembershipPlan
        fields = {
            'name': ['icontains'],
            'price': ['gt', 'lt'],
            'is_active': ['exact'],
            'duration_days': ['gt', 'lt'],
        }
