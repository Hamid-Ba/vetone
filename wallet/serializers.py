from rest_framework import serializers

from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    """Wallet Serializer"""

    class Meta:
        model = Wallet
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction Serializer"""

    class Meta:
        model = Transaction
        fields = "__all__"
