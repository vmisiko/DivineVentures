from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import Mpesa_checkout, Mpesa_c2b_checkout
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from divineVentures.mpesa.LipaNaMpesa import lipa_na_mpesa
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import LNMOnlineSerializer,C2bSerializer
from paypal.standard.forms import PayPalPaymentsForm
from . models  import LNMOnline,C2bTransaction

from Home.models  import Profile


# Create your views here.

# view for mpesa
@login_required
def view_for_mpesa(request):
    
    form = Mpesa_checkout()
    form2 = Mpesa_c2b_checkout()
            
    context = {"form": form,
                "form2" : form2
    }
    
    return render(request, "mpesatemp/payment_via_mpesa.html", context)


@csrf_exempt
def lnm_validate_post(request):
    data = {}  
    callbackurl = request.build_absolute_uri(reverse('MpesaApp:lnm-callbackurl'))
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
