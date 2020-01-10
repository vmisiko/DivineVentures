from django.db import models
from pinax.referrals.models import Referral
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    referral = models.OneToOneField(Referral,on_delete=models.CASCADE,primary_key=True,)
    referrer = models.CharField(max_length = 50, default = "None")
    referred = models.IntegerField(default = 0)
    paid = models.BooleanField(default = False)
    referrals_paid = models.IntegerField(default = 0)
    amount = models.IntegerField(default = 0)

    # referral_response = models.OneToOneField(Referral,on_delete=models.CASCADE, null= True,  related_name = "response_for_referral")


class WithdrawPayouts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    first_name= models.CharField(max_length = 20,)
    last_name = models.CharField(max_length = 20,blank = True, null = True)
    phone_number = models.CharField(max_length = 15,blank = True, null = True)
    email = models.CharField(max_length = 50)
    amount = models.IntegerField(default = 0)
    referrals = models.IntegerField(default = 0,)
    date = models.DateTimeField(auto_now_add = True, blank = True, null = True )
    payment_mode = models.CharField(max_length = 20,blank = True, null = True)
    status = models.BooleanField(default= False)
    


