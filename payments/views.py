from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_payment_history(request):
    payments = Payment.objects.filter(member=request.user).order_by('-created_at')
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_invoice(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id,
        member=request.user
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment.id}.pdf"'

    doc = SimpleDocTemplate(response)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"Invoice ID: {payment.id}", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Amount: {payment.amount} BDT", styles["Normal"]))
    elements.append(Paragraph(f"Status: {payment.status}", styles["Normal"]))
    elements.append(Paragraph(f"Date: {payment.created_at.date()}", styles["Normal"]))

    doc.build(elements)

    return response

