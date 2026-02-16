from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from accounts.permissions import IsAdminOrStaff
from memberships.models import Subscription
from rest_framework import serializers

class AttendanceViewSet(ModelViewSet):
    """
    Attendance Management API

    Used to track attendance of members
    for fitness classes.

    Access:
    - Admin: Full access
    - Staff: Create and view attendance
    - Member: only see

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
        queryset = Attendance.objects.select_related(
            'member',
            'fitness_class'
        )

        # Superuser / Staff → see all
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset

        # Member → see only own
        return queryset.filter(member=self.request.user)

    def perform_create(self, serializer):
        member = serializer.validated_data.get("member")

        if not Subscription.objects.filter(
            user=member,
            is_active=True
        ).exists():
            raise serializers.ValidationError(
                "User does not have an active membership."
            )

        serializer.save()

