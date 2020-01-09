
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from . models  import Profile,LNMOnline,WithdrawPayouts,C2bTransaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from pinax.referrals.models import Referral,ReferralResponse

### mpesa imports 
from .forms import Mpesa_checkout, Mpesa_c2b_checkout,Mpesa_withwraw,Paypal_withdraw
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from divineVentures.mpesa.LipaNaMpesa import lipa_na_mpesa
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import LNMOnlineSerializer,C2bSerializer
from paypal.standard.forms import PayPalPaymentsForm




# Create your views here.


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



# view for mpesa
@login_required
def view_for_mpesa(request):
    
    form = Mpesa_checkout()
    form2 = Mpesa_c2b_checkout()
            
    context = {"form": form,
                "form2" : form2
    }
    
    return render(request, "payment_via_mpesa.html", context)


@csrf_exempt
def lnm_validate_post(request):
    data = {}  
    callbackurl = request.build_absolute_uri(reverse('Home:lnm-callbackurl'))
    print(callbackurl, " this is callbackuri")
    phone_number = request.GET.get('phone_number', None)
    print(phone_number)
    if phone_number:
        
        try: 
            lipa_na_mpesa(phone_number = phone_number, amount = 500, callbackurl = callbackurl, AccountReference = "123456" )

            data["message"] = "Stk-push Successful!! \n Enter The mpesa code "
                
            return JsonResponse(data)
           
                
        except:
            # messages.warning(request, " Type in the correct Phone Number ")
            data[" err_message"] =  " Type in the correct Phone Number "
            return JsonResponse(data)
    else :
        # messages.warning(request, " The form is not valid ")
        data[" err_message"] =  " Type in the correct Phone Number "
        return JsonResponse(data)

@csrf_exempt
def validate_mpesa_code(request):
    profile = Profile.objects.filter(user = request.user,  paid = False).first()
    # amount = order.get_total()
    data = {}  
    mpesa_code = request.GET.get('mpesa_code', None)
    if profile:
        if mpesa_code:
            result1 = LNMOnline.objects.filter( MpesaReceiptNumber__iexact = mpesa_code, paid = False).exists()
            
            if result1 == True: 

                result = LNMOnline.objects.get(MpesaReceiptNumber = mpesa_code, paid = False)
                
                result.paid = True

                result.save()

                Referral.record_response(request, "PAID"  )
                profile.paid = True
                profile.save()

                data["message"] = "Transaction Successful"
                
                return JsonResponse(data)


            else:

                data["message"] = "Mpesa Code Does not exist"
                    
                return JsonResponse(data)
        else:
            data["message"] = "Enter Mpesa Code"
                    
            return JsonResponse(data)
    else:

        data["message"] = "user does not exist"
                    
        return JsonResponse(data)



class LNMCallbackUrl(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer

    permission_classes = [AllowAny]


    def create(self, request):
        print(request.data, "this is data")
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]

        try:
            if result_description != "[STK_CB - ]DS timeout.":

                merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
                print(merchant_request_id)
                checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
                print(checkout_request_id)
                result_code = request.data["Body"]["stkCallback"]["ResultCode"]
                print(result_code)
                result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
                print(result_description)
                amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
                print(amount)
                mpesa_reciept_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"] 
                print(mpesa_reciept_number)
                # balance = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][2]["Value"]
                # print(balance)
                transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
                print(transaction_date)
                phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
                print(phone_number) 

            else:
                print('the result descrption is timeout')
        except:
            print("error result failed")

        from datetime import datetime
        str_transaction_date = str(transaction_date)
        print(str_transaction_date)
        transaction_datetime = datetime.strptime(str_transaction_date,"%Y%m%d%H%M%S")
        print(transaction_datetime) 

        transaction = LNMOnline.objects.create(
            MerchantRequestID  = merchant_request_id,
            CheckoutRequestID = checkout_request_id,
            ResultCode = result_code,
            ResultDesc = result_description,
            Amount = amount,
            MpesaReceiptNumber = mpesa_reciept_number,
            Balance = 0,
            TranscationDate = transaction_datetime,
            PhoneNumber = phone_number
        )
        
        transaction.save() 
        
        data = {
             "result_code" :result_code ,
             "amount": amount

                 }

        

        return Response(data)

class C2bCallbackUrl(CreateAPIView):
    queryset = C2bTransaction.objects.all()
    serializer_class = C2bSerializer
    permission_classes = [AllowAny]


    def create(self, request):
        print(request.data, "this is data")
        # result_description = request.data
        TransactionType =request.data["TransactionType"]
        TransID =request.data["TransID"]
        TransTime =request.data["TransTime"]
        TransAmount =request.data["TransAmount"]
        BusinessShortCode =request.data["BusinessShortCode"]
        BillRefNumber =request.data["BillRefNumber"]
        InvoiceNumber =request.data["InvoiceNumber"]
        OrgAccountBalance =request.data["OrgAccountBalance"]
        ThirdPartyTransID =request.data["ThirdPartyTransID"]
        MSISDN =request.data["MSISDN"]
        FirstName =request.data["FirstName"]
        MiddleName =request.data["MiddleName"]
        LastName =request.data["LastName"]
   

        from datetime import datetime
        str_transaction_date = str(TransTime)
        print(str_transaction_date)
        transaction_datetime = datetime.strptime(str_transaction_date,"%Y%m%d%H%M%S")
        print(transaction_datetime) 

        transaction = C2bTransaction.objects.create(
            TransactionType  = TransactionType,
            TransID = TransID,
            TransTime = transaction_datetime,
            TransAmount = TransAmount,
            BusinessShortCode = BusinessShortCode,
            BillRefNumber = BillRefNumber,
            InvoiceNumber = InvoiceNumber,
            OrgAccountBalance = OrgAccountBalance,
            ThirdPartyTransID = ThirdPartyTransID,
            MSISDN = MSISDN,
            FirstName = FirstName,
            MiddleName = MiddleName,
            LastName = LastName
        )
        
        transaction.save() 
        
        

        return Response({"yey ": "it worked bwana again"})


   

@csrf_exempt
def payment_done(request):
    
    return render(request, 'payment_done.html' ,{})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')


def view_paypal(request):
    7
    order = Profile.objects.get(user = request.user,  paid = False)

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





        payout = WithdrawPayouts(
            user = request.user,
            first_name = first_name,
            last_name= last_name,
            phone_number= phone_number,
            email = email,
            amount = amount,
            referrals = current ,
            payment_mode= "Mpesa"
        )
        payout.save()

        profile.referrals_paid = last + current
        profile.amount = 0
        profile.save()
       
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





        payout = WithdrawPayouts(
            user = request.user,
            first_name = first_name,
            last_name= last_name,
            phone_number= phone_number,
            email = email,
            amount = amount,
            referrals = current ,
            payment_mode= "Paypal"
        )
        payout.save()

        profile.referrals_paid = last + current
        profile.amount = 0
        profile.save()
       
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