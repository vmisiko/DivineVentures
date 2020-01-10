from django.contrib import admin
from .models import Profile,WithdrawPayouts
import random 
import string
from . payout import paypal_payout_release
from django.contrib import messages

sender_batch_id =''.join(
    random.choice(string.ascii_uppercase) for i in range(12)
        
    )




class UserProfile(admin.ModelAdmin):
    
    list_display = ["user" , "referral", "referrer", "referred", "paid",]

admin.site.register(Profile, UserProfile)

# class LNMOnlineAdmin(admin.ModelAdmin):
#     list_display = ["Amount",
#                     "MpesaReceiptNumber",
#                     "TranscationDate",
#                     "PhoneNumber",
#                     "paid"
#                  ]

# admin.site.register(LNMOnline,LNMOnlineAdmin)

class WithdrawPayoutsAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name" ,"phone_number","amount","date","payment_mode","status",]
    actions = ["apply_payout", "apply_Mpesa_payout"]

    def apply_payout(self, request, queryset):
        qs = queryset.filter(payment_mode = "Paypal" ,status = False)
        items = [ ]
       
        for q in qs:       
            payout = {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": q.amount,
                    "currency": "USD"
                },
                "receiver": q.email,
                "note": "congratulations and thank you for working with Divine ventures, keep up the spirit.",
                "sender_item_id": sender_batch_id,
            }
            items.append(payout)
        qs.update(status = True)
        

        # print(items)
        paypal_payout_release(items)
        messages.info(request, "Paypal payment is in process, you will receive notification when it has completed successfully")
    apply_payout.short_description = "Apply payout for paypal"

#     def apply_Mpesa_payout(self, request, queryset):

#         qs = queryset.filter(payment_mode = "Mpesa" )
#         print(len(qs), "is the number of mpesa users")

#         messages.warning(request, "Mpesa payout not yet implemented" )
    
#     apply_Mpesa_payout.short_description = " Apply payout for Mpesa"

# admin.site.register(WithdrawPayouts,WithdrawPayoutsAdmin )

# class C2bTransactionAdmin(admin.ModelAdmin):
#     list_display = ["TransID",
#                     "TransTime",
#                     "TransAmount",
#                     "OrgAccountBalance",
#                     "MSISDN"
#                  ]
# admin.site.register( C2bTransaction , C2bTransactionAdmin)