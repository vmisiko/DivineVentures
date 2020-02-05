from django.contrib import admin
from .models import LNMOnline,C2bTransaction, B2cTransaction
from django.contrib import messages

# Register your models here.

class LNMOnlineAdmin(admin.ModelAdmin):
    list_display = ["Amount",
                    "MpesaReceiptNumber",
                    "TranscationDate",
                    "PhoneNumber",
                    "paid"
                 ]

admin.site.register(LNMOnline,LNMOnlineAdmin)



class C2bTransactionAdmin(admin.ModelAdmin):
    list_display = ["TransID",
                    "TransTime",
                    "TransAmount",
                    "OrgAccountBalance",
                    "MSISDN"
                 ]
admin.site.register( C2bTransaction , C2bTransactionAdmin)

class B2cTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "TransactionID",
        "TransactionAmount",
        "B2CWorkingAccountAvailableFunds",
        "TransactionCompletedDateTime",
        "ReceiverPartyPublicName",
    ]

admin.site.register( B2cTransaction , B2cTransactionAdmin)