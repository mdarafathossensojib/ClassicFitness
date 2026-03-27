from django_filters.rest_framework import FilterSet
from classes.models import FitnessClass

class FitnessClassFilter(FilterSet):
    class Meta:
        model = FitnessClass
        fields = {
            'level': ['exact', 'icontains'],
            'instructor__name': ['exact', 'icontains'],
            'class_date': ['exact', 'gte', 'lte'],
            'start_time': ['exact', 'gte', 'lte'],
            'end_time': ['exact', 'gte', 'lte'],

        }
