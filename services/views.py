from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from services.models import GymService, GymGallery
from services.serializers import GymServiceSerializer, GymGallerySerializer
from accounts.permissions import IsAdminOrReadOnly

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

