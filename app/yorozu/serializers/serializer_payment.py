from rest_framework import serializers
from ..models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """stripeを使った決済関連のserialier"""

    class Meta:
        model = Payment
        # fields = ('id', 'price')
        fields = "__all__"
