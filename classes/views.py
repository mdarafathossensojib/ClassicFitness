from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from classes.models import FitnessClass, ClassBooking
from classes.serializers import FitnessClassSerializer, ClassBookingSerializer, BookClassSerializer
from accounts.permissions import IsAdmin, HasActiveSubscription


# Create your views here.

class FitnessClassViewSet(viewsets.ModelViewSet):
    """
    Fitness Class Management API
    Handles all operations related to gym fitness classes
    - Admin: Full CRUD access
    - Staff: Read access
    - Member: View, Book classes(only subscription member)
    """

    queryset = FitnessClass.objects.select_related('instructor').prefetch_related('bookings').all()

    def get_serializer_class(self):
        if self.action == 'book':
            return BookClassSerializer
        return FitnessClassSerializer

    def get_permissions(self):
        """
        - List & Retrieve: Public
        - Create/Update/Delete: Admin only
        - Book & My Booking: Authenticated users
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        
        if self.action == 'book':
            return [permissions.IsAuthenticated(), HasActiveSubscription()]

        if self.action == 'my_booking':
            return [permissions.IsAuthenticated()]

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]

        return [permissions.IsAuthenticated()]


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def book(self, request, pk=None):
        fitness_class = self.get_object()

        # capacity check
        if fitness_class.bookings.count() >= fitness_class.capacity:
            return Response(
                {'detail': 'Class is full'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # duplicate booking check
        if ClassBooking.objects.filter(
            member=request.user,
            fitness_class=fitness_class
        ).exists():
            return Response(
                {'detail': 'You already booked this class'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = ClassBooking.objects.create(
            member=request.user,
            fitness_class=fitness_class
        )

        serializer = ClassBookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_booking(self, request):
        my_classes = ClassBooking.objects.filter(member=request.user)

        if not my_classes.exists():
            return Response(
                {'detail': 'You have not booked any class'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ClassBookingSerializer(my_classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

