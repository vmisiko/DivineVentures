from django.contrib import admin
from . models import Paypal_callbacktb

# Register your models here.


class Paypal_callbacktbAdmin(admin.ModelAdmin):
    list_display = ("payout_batch_id",
                    "batch_status",
                    "time_completed",
                    "amount",
                    "fees",
                    "payments",

                    ) 
  

admin.site.register(Paypal_callbacktb, Paypal_callbacktbAdmin)