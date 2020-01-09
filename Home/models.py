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

class C2bTransaction(models.Model):
    TransactionType = models.CharField(max_length=50,blank= True,null= True)
    TransID = models.CharField(max_length=50,blank= True,null= True)
    TransTime = models.DateTimeField(blank = True,null = True)
    TransAmount = models.CharField(max_length=50,blank= True,null= True)
    BusinessShortCode = models.CharField(max_length=50,blank= True,null= True)
    BillRefNumber = models.CharField(max_length=50,blank= True,null= True)
    InvoiceNumber = models.CharField(max_length=50,blank= True,null= True)
    OrgAccountBalance = models.CharField(max_length=50,blank= True,null= True)
    ThirdPartyTransID = models.CharField(max_length=50,blank= True,null= True)
    MSISDN  = models.CharField(max_length=50,blank= True,null= True)
    FirstName = models.CharField(max_length=50,blank= True,null= True)
    MiddleName = models.CharField(max_length=50,blank= True,null= True)
    LastName = models.CharField(max_length=50,blank= True,null= True)
    paid = models.BooleanField(default = False)

class LNMOnline(models.Model):
    MerchantRequestID= models.CharField(blank = True,null = True,max_length = 50)
    CheckoutRequestID= models.CharField(blank = True,null = True,max_length = 50)
    ResultCode = models.IntegerField(blank = True,null = True)
    ResultDesc = models.CharField(blank = True,null = True, max_length = 50)
    Amount = models.FloatField(blank = True,null = True)
    MpesaReceiptNumber = models.CharField(blank = True,null = True, max_length = 15)
    Balance = models.CharField(default = 0,max_length = 12)
    TranscationDate = models.DateTimeField(blank = True,null = True)
    PhoneNumber = models.CharField(blank = True,null = True, max_length = 15)
    paid = models.BooleanField(default = False)
# Create your models here. 

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
    


