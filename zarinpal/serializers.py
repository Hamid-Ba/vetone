"""
Zarinpal Module Serializers
"""
from rest_framework import serializers
from .models import Payment


class PaymentInputSerializer(serializers.Serializer):
    """Payment Serializer"""

    pay_amount = serializers.DecimalField(
        max_digits=12, decimal_places=3, required=True
    )


class PaymentSerializer(serializers.ModelSerializer):
    """Payment Serializer"""

    class Meta:
        """Meta Class"""

        model = Payment
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep
