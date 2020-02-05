from rest_framework import serializers
from .models import LNMOnline, C2bTransaction, B2cTransaction

class LNMOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LNMOnline
        fields = ['id',"MerchantRequestID",
"CheckoutRequestID",
"ResultCode",
"ResultDesc",
"Amount",
"MpesaReceiptNumber",
"Balance",
"TranscationDate",
"PhoneNumber",
"paid"]
class C2bSerializer(serializers.ModelSerializer):
    class Meta:
        model = C2bTransaction
        fields = ["id",
                "TransactionType",
                "TransID",
                "TransTime",
                "TransAmount",
                "BusinessShortCode",
                "BillRefNumber",
                "InvoiceNumber",
                "OrgAccountBalance",
                "ThirdPartyTransID",
                "MSISDN",
                "FirstName",
                "MiddleName",
                "LastName",
        ]

class B2cSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2cTransaction
        fields = [
            "TransactionID",
            "TransactionAmount",
            "B2CWorkingAccountAvailableFunds",
            "B2CUtilityAccountAvailableFunds",
            "TransactionCompletedDateTime",
            "ReceiverPartyPublicName",
            "B2CChargesPaidAccountAvailableFunds",
            "B2CRecipientIsRegisteredCustomer",
        ]