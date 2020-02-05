
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from . models  import Profile,WithdrawPayouts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from pinax.referrals.models import Referral,ReferralResponse

### mpesa imports 
from .forms import Mpesa_withwraw,Paypal_withdraw
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from divineVentures.mpesa.LipaNaMpesa import lipa_na_mpesa
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# from .serializers import LNMOnlineSerializer,C2bSerializer
from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.

def example(request):
    
    return render(request, 'sucess.html' ,{})

class Homepage(generic.ListView):
    
    model = Profile
    template_name = "homepage_view.html"


class ReferralPageView(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = "account_view.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ReferralPageView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        referral_code = Profile.objects.get(user = self.request.user)

        referrer_qs = ReferralResponse.objects.filter( user = self.request.user ).first()

        if referrer_qs:


            referrer_confirmed =  Profile.objects.get( referral = referrer_qs.referral)
            print(referrer_confirmed.user)

            referrer = referrer_confirmed.user
            # qs =Referral.objects.get(user = self.request.user, label = "SIGNED_UP" )
            
            
        else:
            referrer = "None"
        qr = ReferralResponse.objects.filter(referral=referral_code.referral, action ="SIGNED_UP"  ).count()
        print(qr, "signed up")

        paid = ReferralResponse.objects.filter(referral=referral_code.referral, action ="PAID"  ).count()

        clicks = ReferralResponse.objects.filter(referral=referral_code.referral, action ="RESPONDED"  ).count()

        not_paid_referrals = paid - referral_code.referrals_paid
        amount = 3 * not_paid_referrals
        print(amount, "pay account balance")

        status_check = referral_code.paid 
        if status_check == True:
            status = "Paid"
        else:
            status = "Not Paid"

        referral_code.amount = amount
        referral_code.referrer = str(referrer)
        referral_code.referred = paid
        referral_code.save()
        # update to profile
        context["balance"] = amount
        context['paid'] = paid
        context["status"] = status
        context["referrer"] = referrer
        context["qr"] = qr
        context["clicks"] = clicks
        context['referral_code'] = referral_code

        return context

class welcomeafterClickin(generic.ListView):
    model = Profile
    template_name = "welcomeforclickers.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(welcomeafterClickin, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        referral = ReferralResponse.objects.filter( session_key = self.request.session.session_key  ).first()
        print(referral.referral)

        referral_code = Profile.objects.get(referral = referral.referral)
        print(referral_code.user)

        context['referrer'] = referral_code.user

        return context
  

@csrf_exempt
def payment_done(request):
    
    return render(request, 'payment_done.html' ,{})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')


def view_paypal(request):
    
    order = Profile.objects.filter(user = request.user,  paid = False)

    if order:
        print(order.user_id, "this is the cool order number")
        host = request.get_host()
        
        # What you want the button to do.
        paypal_dict = {
            "business": "misikovictor123@gmail.com",
            "amount": "5",
            "item_name":'Order for  {}'.format(order.user),
            "invoice": str(order.user_id),
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('Home:payment-done')),
            "cancel_return": request.build_absolute_uri(reverse('Home:payment-cancelled')),
            "custom": request.user,  # Custom command to correlate to some function later (optional)
        }

        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form,
                    "order":  order
        }

        
        return render(request, "payment.html", context)


    else:
        return render(request, 'alreadypaid.html' ,{})

class WithdrawalView(generic.ListView):
    model = Profile
    template_name = "withdraw.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        referral_code = Profile.objects.get(user = self.request.user)
        payouts = WithdrawPayouts.objects.filter(user = self.request.user).order_by("-date")
        # print(len(payout), "payout history")
        context = super(WithdrawalView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        form = Mpesa_withwraw()
        form2 = Paypal_withdraw() 
        
        
                
        context = {"form": form,
                    "form2": form2,
                    "amount": referral_code.amount,
                    "referral_code": referral_code,
                    "payouts": payouts
                }
    

        return context

def validate_widthrawal(request):
    data = {}  
    profile = Profile.objects.get(user = request.user)
    
    
    form = Mpesa_withwraw(request.POST or None)
    if form.is_valid():
        
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        phone_number = form.cleaned_data.get("phone_number")
        email = form.cleaned_data.get("email")
        amount = profile.amount
        last = profile.referrals_paid
        current = profile.referred - profile.referrals_paid

        dp = 1 + 0.01*int(amount)
        amount_dispensed = amount - dp

        payout = WithdrawPayouts(
            user = request.user,
            first_name = first_name,
            last_name= last_name,
            phone_number= phone_number,
            email = email,
            amount_request = amount,
            amount_dispensed = amount_dispensed,
            referrals = current ,
            payment_mode= "Mpesa"
        )

        payout.save()
        profile.referrals_paid = last + current
        profile.amount = 0
        profile.save()

        span = 0.01*int(amount)
        data["percentage"] = "2"
        data['span'] = span
        data['gross'] = amount
        data["tcharges"]= dp
        data["net"] = amount_dispensed

        print(span, amount, dp, amount_dispensed, "this ire they")
       
        # messages.warning(request, " The form is not valid ")
        data["message"] =  "Withdrawal successful, your money is pending awaiting release"
        return JsonResponse(data)
    else:

        data["message"] =  "Not successful, form not valid"
        return JsonResponse(data)

def validate_Paypal_widthrawal(request):
    data = {}  
    profile = Profile.objects.get(user = request.user)
    
    
    form = Mpesa_withwraw(request.POST or None)
    if form.is_valid():
        
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        phone_number = form.cleaned_data.get("phone_number")
        email = form.cleaned_data.get("email")
        amount = profile.amount
        last = profile.referrals_paid
        current = profile.referred - profile.referrals_paid



        dp = 1 + 0.02*int(amount)
        amount_dispensed = amount - dp

        payout = WithdrawPayouts(
            user = request.user,
            first_name = first_name,
            last_name= last_name,
            phone_number= phone_number,
            email = email,
            amount_request = amount,
            amount_dispensed = amount_dispensed,
            referrals = current ,
            payment_mode= "Paypal"
        )
        payout.save()

        profile.referrals_paid = last + current
        profile.amount = 0
        profile.save()

        span = 0.02*int(amount)

        data["percentage"] = "2"
        data['span'] = span
        data['gross'] = amount
        data["tcharges"]= dp
        data["net"] = amount_dispensed
        
        # messages.warning(request, " The form is not valid ")
        data["message"] =  "Withdrawal successful, your money is pending awaiting release"
        return JsonResponse(data)
    else:

        data["message"] =  "Not successful, form not valid"
        return JsonResponse(data)

    
class PaypalWithdrawalView(generic.ListView):
    model = Profile
    template_name = "paypal_withdrawal.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        referral_code = Profile.objects.get(user = self.request.user)
        payouts = WithdrawPayouts.objects.filter(user = self.request.user).order_by("-date")
        # print(len(payout), "payout history")
        context = super(PaypalWithdrawalView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        form2 = Mpesa_withwraw()
        form = Paypal_withdraw()
        
        
                
        context = {"form": form,
                    "form2": form2,
                    "amount": referral_code.amount,
                    "referral_code": referral_code,
                    "payouts": payouts
                }
    

        return context