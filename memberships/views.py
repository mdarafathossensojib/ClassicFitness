from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from memberships.models import MembershipPlan, Subscription
from memberships.serializers import MembershipPlanSerializer, SubscriptionSerializer, MemberShipSerializer
from accounts.permissions import IsAdminOrReadOnly
from rest_framework import status
from sslcommerz_lib import SSLCOMMERZ
from decouple import config
from django.conf import settings as main_settings
from django.http import HttpResponseRedirect
from payments.models import Payment, Transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from memberships.filters import MembershipPlanFilter


# Create your views here.

class MembershipPlanViewSet(ModelViewSet):
    """
    Membership Plan Management API

    This API manages gym membership plans such as
    Weekly, Monthly, Half-Yearly and Yearly subscriptions.

    Roles:
    - Admin:
        - Create, update, delete membership plans
    - Member:
        - View available plans
    """
    
    queryset = MembershipPlan.objects.filter(is_active=True)
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MembershipPlanFilter
    search_fields = ['name']
    ordering_fields = ['price', 'duration_days']


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




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user
    plan_id = request.data.get('plan_id')

    try:
        plan = MembershipPlan.objects.get(id=plan_id)
    except MembershipPlan.DoesNotExist:
        return Response({"error": "Invalid plan"}, status=400)

    # Create Payment (PENDING)
    payment = Payment.objects.create(
        member=user,
        amount=plan.price,
        status=Payment.STATUS_PENDING
    )

    settings_data = {
        'store_id': config('store_id'),
        'store_pass': config('store_pass'),
        'issandbox': True
    }

    sslcz = SSLCOMMERZ(settings_data)

    post_body = {
        'total_amount': float(plan.price),
        'currency': "BDT",
        'tran_id': f"trxn_{payment.id}",
        'success_url': f"{main_settings.BACKEND_URL}/api/v1/payment/success/",
        'fail_url': f"{main_settings.BACKEND_URL}/api/v1/payment/fail/",
        'cancel_url': f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/",
        'emi_option': 0,
        'cus_name': f"{user.first_name} {user.last_name}",
        'cus_email': user.email,
        'cus_phone': user.phone_number,
        'cus_add1': user.address,
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'num_of_item': 1,
        'product_name': plan.name,
        'product_category': "Membership",
        'product_profile': "general",
    }

    response = sslcz.createSession(post_body)

    if response.get('status') == 'SUCCESS':
        return Response({
            'payment_url': response.get('GatewayPageURL')
        })

    return Response({'error': 'Failed to initiate payment'}, status=400)

@api_view(['POST'])
def payment_success(request):
    tran_id = request.data.get('tran_id')

    payment_id = tran_id.split('_')[1]

    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return Response({"error": "Invalid payment"}, status=400)

    # Update Payment
    payment.status = Payment.STATUS_PAID
    payment.paid_at = timezone.now()
    payment.save()

    # Create Subscription
    plan = MembershipPlan.objects.get(price=payment.amount)

    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=plan.duration_days)

    subscription, created = Subscription.objects.update_or_create(
        user=payment.member,
        defaults={
            'plan': plan,
            'start_date': start_date,
            'end_date': end_date,
            'is_active': True
        }
    )

    payment.subscription = subscription
    payment.save()

    # Save Transaction
    Transaction.objects.create(
        payment=payment,
        gateway_name="SSLCommerz",
        transaction_id=request.data.get('bank_tran_id'),
        raw_response=request.data
    )

    return HttpResponseRedirect(
        f"{main_settings.FRONTEND_URL}/dashboard/payment/success/"
    )

@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/membership-plans/")

@api_view(['POST'])
def payment_fail(request):
    tran_id = request.data.get('tran_id')
    payment_id = tran_id.split('_')[1]

    payment = Payment.objects.filter(id=payment_id).first()
    if payment:
        payment.status = Payment.STATUS_FAILED
        payment.save()

    return HttpResponseRedirect(
        f"{main_settings.FRONTEND_URL}/dashboard/payment/failed/"
    )

