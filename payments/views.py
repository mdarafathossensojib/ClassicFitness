from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_payment_history(request):
    payments = Payment.objects.filter(member=request.user).order_by('-created_at')
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)
