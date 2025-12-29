from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from memberships.models import MembershipPlan, Subscription
from memberships.serializers import MembershipPlanSerializer, SubscriptionSerializer, MemberShipSerializer
from accounts.permissions import IsAdminOrReadOnly


# Create your views here.

class MembershipPlanViewSet(ModelViewSet):
    queryset = MembershipPlan.objects.filter(is_active=True)
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'subscribe':
            return MemberShipSerializer
        return MembershipPlanSerializer

    @action(detail=True,methods=['post'],permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        plan = self.get_object()

        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=plan.duration_days)

        subscription, created = Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                'plan': plan,
                'start_date': start_date,
                'end_date': end_date,
                'is_active': True
            }
        )

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_subscription(self, request):
        subscription = Subscription.objects.filter(
            user=request.user,
            is_active=True
        ).first()

        if not subscription:
            return Response(
                {'detail': 'No active subscription found'},
                status=404
            )

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)



