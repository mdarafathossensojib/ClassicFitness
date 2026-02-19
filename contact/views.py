from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from contact.models import ContactMessage
from contact.serializers import ContactMessageSerializer

class ContactMessageViewSet(ModelViewSet):
    queryset = ContactMessage.objects.all().order_by("-created_at")
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]  
        return [IsAdminUser()]   
    
    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        contact = self.get_object()
        contact.is_read = True
        contact.save()
        return Response({"status": "marked as read"})
