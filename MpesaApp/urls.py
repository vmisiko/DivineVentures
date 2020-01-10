from django.contrib import admin
from django.urls import path
from . import views


app_name = "MpesaApp"

urlpatterns = [
     
    path("lnm_payment/", views.view_for_mpesa, name = "mpesa_payment"),
    path('validate_payment/', views.lnm_validate_post, name = 'validate_payment'),
    path('validate_stk_code/', views.validate_mpesa_code, name = 'validate_mpesa_code'),
    path('lnm/', views.LNMCallbackUrl.as_view(), name = 'lnm-callbackurl'), 
    path('c2b_callback/', views.C2bCallbackUrl.as_view(), name = 'c2b-callbackurl'),
]

