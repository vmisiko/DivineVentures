from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from allauth.account.signals import user_signed_up
from .models import Profile
from pinax.referrals.models import Referral
from paypal.standard.ipn.signals import valid_ipn_received

@receiver(user_signed_up)
def save_profile(sender, **kwargs):
    request = kwargs['request'] 
    user = kwargs['user']
    print(user)
    

    referral = Referral.create(

        user = user,
        redirect_to = reverse("Home:afterclickin"), 
        label ="SIGNED_UP",

    )
    
    Referral.record_response(request, "SIGNED_UP"  )

    

    profile = Profile.objects.create(user= user, referral = referral)
    
    profile.save()


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        # payment was successful
        
        
        profile = Profile.objects.get(user_id = ipn.invoice )
        Referral.record_response(request, "PAID"  )

        profile.paid = True
        profile.save()

