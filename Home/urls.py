from django.contrib import admin
from django.urls import path
from . import views


app_name = "Home"

urlpatterns = [
    
    
    path('', views.Homepage.as_view() , name = "home"), 
    path('home/', views.Homepage.as_view(), name = "home"),
    path('', views.Homepage.as_view() , name = "home"),
    path("profileaccount/", views.ReferralPageView.as_view(), name = "refferal-page"),
    path("afterclickin/", views.welcomeafterClickin.as_view(), name = "afterclickin"),
    # path("lnm_payment/", views.view_for_mpesa, name = "mpesa_payment"),
    # path('validate_payment/', views.lnm_validate_post, name = 'validate_payment'),
    # path('validate_stk_code/', views.validate_mpesa_code, name = 'validate_mpesa_code'),
    # path('lnm/', views.LNMCallbackUrl.as_view(), name = 'lnm-callbackurl'), 
    # path('c2b_callback/', views.C2bCallbackUrl.as_view(), name = 'c2b-callbackurl'),
    path('payment/', views.view_paypal, name = 'payment'),
    path('payment-done/', views.payment_done, name= 'payment-done'),
    path('payment-cancelled/', views.payment_canceled, name = 'payment-cancelled'),
    path('withdraw/', views.WithdrawalView.as_view(), name = 'withdraw'),
    path('paypal_withdraw/', views.PaypalWithdrawalView.as_view(), name = 'paypal_withdraw'),
    path('validate_withdrawal/', views.validate_widthrawal, name = 'validate_withdrawal'),
    path('validate_paypal_withdrawal/', views.validate_Paypal_widthrawal, name = 'validate_paypal_withdrawal'),
]

