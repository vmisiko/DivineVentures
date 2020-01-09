from django.db import models

# Create your models here.

class Paypal_callbacktb(models.Model):
    resultid = models.CharField(max_length = 50,blank = True,null = True)
    payout_batch_id  = models.CharField(max_length = 20,blank = True,null = True)
    batch_status = models.CharField(max_length = 20,blank = True,null = True)
    time_created = models.DateTimeField(blank = True,null = True)
    time_completed = models.DateTimeField(blank = True,null = True)
    sender_batch_id = models.CharField(max_length = 20,blank = True,null = True)
    amount = models.FloatField(default = 0.0)
    currency = models.CharField(max_length = 20,blank = True,null = True)
    fees = models.FloatField(default = 0.0)
    payments = models.IntegerField(default = 0)
