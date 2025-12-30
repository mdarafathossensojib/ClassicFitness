from rest_framework.viewsets import ModelViewSet
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from accounts.permissions import IsAdmin, IsStaff
from memberships.models import Subscription

class AttendanceViewSet(ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdmin, IsStaff]

    def get_queryset(self):
        active_users = Subscription.objects.filter(
            is_active=True
        ).values_list('user_id', flat=True)

        return Attendance.objects.filter(member_id__in=active_users).select_related('member','fitness_class')
