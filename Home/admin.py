from django.contrib import admin
from .models import Profile,WithdrawPayouts
import random 
import string
from . payout import paypal_payout_release
from django.contrib import messages
from .tasks import mpesa_payout_task,paypal_payout_task






class UserProfile(admin.ModelAdmin):
    
    list_display = ["user" , "referral", "referrer", "referred", "paid",]

admin.site.register(Profile, UserProfile)


class WithdrawPayoutsAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name" ,"phone_number","amount_request","amount_dispensed","date","payment_mode","status",]
    actions = ["apply_payout", "mpesa_payout"]

    def apply_payout(self, request, queryset):
        pk_model = []
        for q in queryset:
            pk_model.append(q.pk)
        print(pk_model)
        # mpesa_payout_task.delay(pk_model)
        try:  
            paypal_payout_task.delay(pk_model)
            self.message_user(request, "Please wait this may take a while. Refresh after some few minutes")
        except:
            self.message_user(request, "Failed! Retry again")

    apply_payout.short_description = "Apply Paypal Payout"

    def mpesa_payout(self, request, queryset):
        
        pk_model = []
        for q in queryset:
            pk_model.append(q.pk)
        print(pk_model)
        # mpesa_payout_task.delay(pk_model)
        try:  
            mpesa_payout_task.delay(pk_model)
            self.message_user(request, "Please wait this may take a while. Refresh after some few minutes")
        except:
            self.message_user(request, "Failed! Retry again")
    mpesa_payout.short_description = "Apply Mpesa Payout"

admin.site.register(WithdrawPayouts, WithdrawPayoutsAdmin)
