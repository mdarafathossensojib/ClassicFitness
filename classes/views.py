from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from classes.models import FitnessClass, ClassBooking, Trainer
from classes.serializers import FitnessClassSerializer, ClassBookingSerializer, BookClassSerializer, TrainerSerializer
from accounts.permissions import IsAdmin, HasActiveSubscription
from classes.paginations import DefaultPagination, TrainerPagination
from classes.filters import FitnessClassFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


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
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FitnessClassFilter
    search_fields = ['title', 'description']
    ordering_fields = ['start_time', 'end_time', 'capacity']

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


    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        fitness_class = self.get_object()
    
        # capacity check
        if fitness_class.bookings.filter(is_cancelled=False).count() >= fitness_class.capacity:
            return Response(
                {'detail': 'Class is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        # duplicate booking check
        if ClassBooking.objects.filter(
            member=request.user,
            fitness_class=fitness_class,
            is_cancelled=False
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
    

    @action(detail=False, methods=['get'])
    def my_booking(self, request):
        my_classes = ClassBooking.objects.filter(
            member=request.user,
            is_cancelled=False
        ).select_related('fitness_class')
    
        serializer = ClassBookingSerializer(my_classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel_booking(self, request, pk=None):
        booking = ClassBooking.objects.filter(
            id=pk,
            member=request.user
        ).first()
    
        if not booking:
            return Response(
                {'detail': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
        booking.is_cancelled = True
        booking.save()
    
        return Response({'detail': 'Booking cancelled successfully'})


class TrainerViewSet(viewsets.ModelViewSet):
    """
    Trainer Management API
    Handles all operations related to gym trainers
    - Admin: Full CRUD access
    - Staff & Member: Read access
    """

    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    pagination_class = TrainerPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'specialty']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]

        return [permissions.IsAuthenticated()]
