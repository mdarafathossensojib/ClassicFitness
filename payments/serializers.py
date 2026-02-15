from rest_framework import serializers
from payments.models import Payment, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "gateway_name",
            "transaction_id",
            "created_at"
        ]


class PaymentSerializer(serializers.ModelSerializer):
    transaction = serializers.SerializerMethodField()
    plan_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "status",
            "paid_at",
            "created_at",
            "plan_name",
            "transaction"
        ]

    def get_transaction(self, obj):
        transaction = getattr(obj, "transaction", None)
        if transaction:
            return TransactionSerializer(transaction).data
        return None

    def get_plan_name(self, obj):
        if obj.subscription:
            return obj.subscription.plan.name
        return None
