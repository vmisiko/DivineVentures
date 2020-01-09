
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import Paypal_callbacktbSerializer
from . models import Paypal_callbacktb
# Create your views here.

class Paypal_callback(CreateAPIView):
    queryset = Paypal_callbacktb.objects.all()
    serializer_class = Paypal_callbacktbSerializer
    permission_classes = [AllowAny] 

    def create(self, request):
        result = request.data
        print(request.data, "this is data")
        resultid = result["id"]
        
        payout_batch_id = result["resource"]["batch_header"]["payout_batch_id"]
        
        batch_status = result["resource"]["batch_header"]["batch_status"]
        time_created = result["resource"]["batch_header"]["time_created"]
        time_completed =result["resource"]["batch_header"]["time_completed"]
        
        sender_batch_id = result["resource"]["batch_header"]["sender_batch_header"]["sender_batch_id"]
        amount = result["resource"]["batch_header"]["amount"]["value"]
        
        currency = result["resource"]["batch_header"]["amount"]["currency"]
        
        fees = result["resource"]["batch_header"]["fees"]["value"]
        payment = result["resource"]["batch_header"]["payments"]

        # from datetime import datetime
        # str_time_created = str(time_created)
        # str_time_completed = str(time_completed)
        
        # created_datetime = datetime.strptime(str_time_created,"%Y%m%d%H%M%S")
        # completed_datetime = datetime.strptime(str_time_completed,"%Y%m%d%H%M%S")
        # print(created_datetime) 
        # print(completed_datetime)



        payout = Paypal_callbacktb.objects.create(
                    resultid = resultid,
                    payout_batch_id = payout_batch_id,
                    batch_status = batch_status,
                    time_created = time_created,
                    time_completed = time_completed,
                    sender_batch_id = sender_batch_id,
                    amount = amount,
                    currency = currency,
                    fees = fees,
                    payments = payment,
        )
        payout.save()

        return Response({"yey":"it is working!"})

class HowitWorksView(generic.ListView):
    
    model = Paypal_callbacktb
    template_name = "payouts/how_it_works.html"

class ContactView(generic.ListView):
    
    model = Paypal_callbacktb
    template_name = "payouts/contacts.html"