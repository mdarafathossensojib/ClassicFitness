from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from services.models import GymService, GymGallery, Feedback
from services.serializers import GymServiceSerializer, GymGallerySerializer, FeedbackSerializer
from accounts.permissions import IsAdminOrReadOnly

class GymServiceViewSet(ModelViewSet):
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
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        class_id = self.kwargs.get('class_pk')
        qs = Feedback.objects.filter(fitness_class_id=class_id)

        user = self.request.user
        if not user.is_staff and not user.is_superuser:
            qs = qs.filter(member=user)
        return qs

    def perform_create(self, serializer):
        class_id = self.kwargs.get('class_pk')
        serializer.save(fitness_class_id=class_id, member=self.request.user)
