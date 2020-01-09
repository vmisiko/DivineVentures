from rest_framework import serializers
from .models import Paypal_callbacktb

class Paypal_callbacktbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paypal_callbacktb
        fields = [
            "payout_batch_id",
            "batch_status",
            "time_completed",
            "amount",
            "fees",
            "payments",
        ]

