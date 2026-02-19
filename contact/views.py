from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from contact.models import ContactMessage
from contact.serializers import ContactMessageSerializer

class ContactMessageViewSet(ModelViewSet):
    queryset = ContactMessage.objects.all().order_by("-created_at")
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]  
        return [IsAdminUser()]   
