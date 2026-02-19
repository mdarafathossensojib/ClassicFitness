from rest_framework.viewsets import ModelViewSet
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from accounts.permissions import IsAdminOrStaff
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from classes.models import FitnessClass, ClassBooking
from django.db.models import Count, Q


class AttendanceViewSet(ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'class_summary', 'booked_users']:
            return [IsAdminOrStaff()]
        return [IsAuthenticated()]


    def get_queryset(self):
        queryset = Attendance.objects.select_related(
            'member',
            'fitness_class'
        )

        class_id = self.request.query_params.get("fitness_class")

        if class_id:
            queryset = queryset.filter(fitness_class_id=class_id)

        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset

        return queryset.filter(member=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    # Get booked users for selected class
    @action(detail=False, methods=['get'], url_path='booked-users')
    def booked_users(self, request):
        class_id = request.query_params.get('class_id')

        bookings = ClassBooking.objects.filter(
            fitness_class_id=class_id,
            is_cancelled=False
        ).select_related('member')

        data = [
            {
                "member_id": b.member.id,
                "member_name": b.member.get_full_name(),
                "email": b.member.email
            }
            for b in bookings
        ]

        return Response(data)

    #Class Attendance Summary
    @action(detail=False, methods=['get'], url_path='class-summary')
    def class_summary(self, request):
        classes = FitnessClass.objects.all()

        result = []

        for cls in classes:
            total_booked = cls.bookings.filter(is_cancelled=False).count()

            present = cls.attendances.filter(is_present=True).count()
            absent = total_booked - present

            result.append({
                "class_id": cls.id,
                "class_title": cls.title,
                "present_count": present,
                "absent_count": absent
            })

        return Response(result)
    
    @action(detail=False, methods=['get'])
    def my_summary(self, request):
        queryset = Attendance.objects.filter(
            member=request.user
        ).values(
            'fitness_class',
            'fitness_class__title'
        ).annotate(
            present_count=Count('id', filter=Q(is_present=True)),
            absent_count=Count('id', filter=Q(is_present=False))
        )

        data = [
            {
                "class_id": item["fitness_class"],
                "class_title": item["fitness_class__title"],
                "present_count": item["present_count"],
                "absent_count": item["absent_count"],
            }
            for item in queryset
        ]

        return Response(data)


