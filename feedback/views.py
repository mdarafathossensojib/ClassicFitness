from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from feedback.models import ClassFeedback, Feedback
from feedback.serializers import FeedbackSerializer, ClassFeedbackSerializer
from accounts.permissions import IsOwnerOrAdminStaff
from classes.models import FitnessClass
from django.shortcuts import get_object_or_404
# Create your views here.


class FeedbackViewSet(ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminStaff]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Feedback.objects.none()

        return Feedback.objects.select_related('member').all()

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)


class ClassFeedbackViewSet(ModelViewSet):
    """
    Class Feedback API (Nested Resource)

    This API allows members to leave feedback
    for fitness classes they attended.

    URL Pattern:
    - /classes/{class_id}/feedback/

    Roles:
    - Member:
        - Create feedback for a class
        - View feedback
    - Admin / Staff:
        - View all feedback for a class

    Rules:
    - One feedback per member per class
    - Member identity auto-assigned
    """
      
    serializer_class = ClassFeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminStaff]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ClassFeedback.objects.none()

        class_id = self.kwargs.get('class__pk')
        return ClassFeedback.objects.filter(fitness_class_id=class_id).select_related('member')

    def perform_create(self, serializer):
        fitness_class = get_object_or_404(
            FitnessClass,
            pk=self.kwargs.get('class__pk')
        )
        serializer.save(
            member=self.request.user,
            fitness_class=fitness_class
        )
