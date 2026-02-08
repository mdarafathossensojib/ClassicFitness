from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
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
def initiate_payment(request):
    user = request.user
    amount = request.data.get('amount')
    order_id = request.data.get('orderId')

    settings = { 'store_id': config('store_id'), 'store_pass': config('store_pass'), 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"trxn_{order_id}"
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Membership Subscription"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    
    if response.get('status') == 'SUCCESS':
        return Response({'payment_url': response.get('GatewayPageURL')})
    
    return Response({'error': 'Failed to initiate payment'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def payment_success(request):
    order_id = request.data.get('tran_id').split('_')[1]
    order = Subscription.objects.get(id=order_id)
    order.status = 'Ready To Ship'
    order.save()

    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/payment/success/")

@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")

@api_view(['POST'])
def payment_fail(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")
