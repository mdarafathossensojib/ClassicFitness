from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from services.models import GymService, GymGallery, Feedback
from services.serializers import GymServiceSerializer, GymGallerySerializer, FeedbackSerializer
from accounts.permissions import IsAdminOrReadOnly
from classes.models import FitnessClass
from django.shortcuts import get_object_or_404

class GymServiceViewSet(ModelViewSet):
    """
    Gym Services API

    Manages services provided by the gym
    such as Personal Training, Nutrition Coaching,
    Cardio Zone, etc.

    Roles:
    - Admin:
        - Create, update, delete services
    - Public:
        - View active gym services

    Endpoints:
    - GET    /services/
        List gym services
    - POST   /services/
        Create a service (Admin only)
    """

    queryset = GymService.objects.all()
    serializer_class = GymServiceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []


class GymGalleryViewSet(ModelViewSet):
    queryset = GymGallery.objects.all()
    serializer_class = GymGallerySerializer
    permission_classes = [IsAdminOrReadOnly]


class FeedbackViewSet(ModelViewSet):
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
      
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Feedback.objects.none()

        class_id = self.kwargs.get('class__pk')
        return Feedback.objects.filter(
            fitness_class_id=class_id,
            member=self.request.user
        )

    def perform_create(self, serializer):
        fitness_class = get_object_or_404(
            FitnessClass,
            pk=self.kwargs.get('class__pk')
        )
        serializer.save(
            member=self.request.user,
            fitness_class=fitness_class
        )
