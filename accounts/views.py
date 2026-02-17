from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers import UserProfileUpdateSerializer
from django.utils import timezone
from attendance.models import Attendance
from classes.models import ClassBooking
from memberships.models import Subscription


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileUpdateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # Active Membership
        subscription = Subscription.objects.filter(
            user=user,
            is_active=True,
            end_date__gte=today
        ).select_related("plan").first()

        # This month attendance
        start_month = today.replace(day=1)

        attended_this_month = Attendance.objects.filter(
            member=user,
            is_present=True,
            marked_at__date__gte=start_month
        ).count()

        total_attended = Attendance.objects.filter(
            member=user,
            is_present=True
        ).count()

        # upcoming class
        upcoming_classes = ClassBooking.objects.filter(
            member=user,
            is_cancelled=False,
            fitness_class__class_date__gte=today
        ).select_related("fitness_class")

        upcoming_data = [
            {
                "title": booking.fitness_class.title,
                "date": booking.fitness_class.class_date,
            }
            for booking in upcoming_classes
        ]

        # Recent attendance
        recent_activity = Attendance.objects.filter(
            member=user
        ).order_by("-marked_at")[:5]

        activity_data = [
            {
                "class": att.fitness_class.title,
                "date": att.marked_at,
                "present": att.is_present
            }
            for att in recent_activity
        ]

        return Response({
            "membership": {
                "plan": subscription.plan.name if subscription else None,
                "expiry": subscription.end_date if subscription else None,
            },
            "stats": {
                "attended_this_month": attended_this_month,
                "total_attended": total_attended,
            },
            "upcoming_classes": upcoming_data,
            "recent_activity": activity_data
        })
