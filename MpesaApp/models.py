from django.db import models

# Create your models here.

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
