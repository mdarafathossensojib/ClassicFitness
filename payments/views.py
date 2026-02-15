from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_payment_history(request):
    payments = Payment.objects.filter(member=request.user).order_by('-created_at')
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


def download_invoice(request, invoice_id):
    payment = Payment.objects.get(invoice_id=invoice_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoice_id}.pdf"'

    doc = SimpleDocTemplate(response)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Invoice ID: {payment.invoice_id}", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Amount: ${payment.amount}", styles["Normal"]))
    elements.append(Paragraph(f"Status: {payment.status}", styles["Normal"]))

    doc.build(elements)

    return response

