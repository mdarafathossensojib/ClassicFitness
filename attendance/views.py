from rest_framework.viewsets import ModelViewSet
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from accounts.permissions import IsAdminOrStaff
from memberships.models import Subscription

class AttendanceViewSet(ModelViewSet):
    """
    Attendance Management API

    Used to track attendance of members
    for fitness classes.

    Access:
    - Admin: Full access
    - Staff: Create and view attendance
    - Member: No access

    Rules:
    - Only members with active subscriptions
      can be marked as present
    - Each member can have only one
      attendance record per class

    Endpoints:
    - GET    /attendance/
        View attendance records
    - POST   /attendance/
        Mark attendance for a class(Only Subscription Member)
    """
    
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrStaff]

    def get_queryset(self):
        active_users = Subscription.objects.filter(
            is_active=True
        ).values_list('user_id', flat=True)

        return Attendance.objects.filter(member_id__in=active_users).select_related('member','fitness_class')
