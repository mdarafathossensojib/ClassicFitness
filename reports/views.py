from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Avg
from attendance.models import Attendance
from django.utils import timezone
from memberships.models import Subscription
from django.db.models.functions import TruncMonth
from datetime import timedelta
from services.models import Feedback
from classes.models import FitnessClass

class AttendanceSummaryReport(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total = Attendance.objects.count()
        present = Attendance.objects.filter(is_present=True).count()
        absent = Attendance.objects.filter(is_present=False).count()

        by_class = (
            Attendance.objects.values('fitness_class__title').annotate(total=Count('id'))
        )

        return Response({
            "total_records": total,
            "present": present,
            "absent": absent,
            "by_class": by_class
        })


class MembershipStatusReport(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.now().date()

        active = Subscription.objects.filter(
            is_active=True,
            end_date__gte=today
        ).count()

        expired = Subscription.objects.filter(
            end_date__lt=today
        ).count()

        return Response({
            "active_memberships": active,
            "expired_memberships": expired
        })



class MembershipPlanReport(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = (
            Subscription.objects.filter(is_active=True).values('plan__name').annotate(total_members=Count('id'))
        )

        return Response(data)



class MonthlyMembershipReport(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = (
            Subscription.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id')).order_by('month')
        )

        return Response(data)


class MembershipExpirySoonReport(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        next_week = today + timedelta(days=7)

        expiring = Subscription.objects.filter(
            end_date__range=[today, next_week]
        ).values(
            'user__email',
            'plan__name',
            'end_date'
        )

        return Response(expiring)


class FeedbackReportAPIView(APIView):
    permission_classes = [IsAdminUser] 

    def get(self, request):
        data = Feedback.objects.values('fitness_class__title').annotate(
            average_rating=Avg('rating'),
            total_reviews=Count('id')
        ).order_by('-average_rating')

        rating_dist = Feedback.objects.values('fitness_class__title', 'rating').annotate(
            count=Count('id')
        ).order_by('fitness_class__title', 'rating')

        return Response({
            "class_summary": list(data),
            "rating_distribution": list(rating_dist)
        })

