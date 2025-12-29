from rest_framework import serializers
from classes.models import FitnessClass, ClassBooking

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    booked_count = serializers.IntegerField(source='bookings.count', read_only=True)

    class Meta:
        model = FitnessClass
        fields = [
            'id', 'title', 'description', 'instructor', 'instructor_name',
            'class_date', 'start_time', 'end_time', 'capacity', 'booked_count', 'image'
        ]
        read_only_fields = ['booked_count', 'instructor_name']


class ClassBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassBooking
        fields = ['id', 'fitness_class', 'member', 'booked_at', 'is_cancelled']
        read_only_fields = ['member', 'booked_at']


class BookClassSerializer(serializers.Serializer):
    pass

