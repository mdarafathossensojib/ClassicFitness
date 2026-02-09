from rest_framework import serializers
from classes.models import FitnessClass, ClassBooking, Trainer

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    booked_count = serializers.IntegerField(source='bookings.count', read_only=True)

    class Meta:
        model = FitnessClass
        fields = [
            'id', 'title', 'level', 'description', 'longDescription', 'benefits', 'whatToExpect', 'instructor', 'instructor_name', 'class_date', 'start_time', 'end_time', 'capacity', 'booked_count', 'image'
        ]
        read_only_fields = ['booked_count', 'instructor_name']

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ['id', 'name', 'role', 'image', 'rating', 'experience', 'certifications', 'clients', 'specialties', 'bio', 'philosophy', 'schedule']
        

class ClassBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassBooking
        fields = ['id', 'fitness_class', 'member', 'booked_at', 'is_cancelled']
        read_only_fields = ['member', 'fitness_class', 'booked_at']


class BookClassSerializer(serializers.Serializer):
    pass

