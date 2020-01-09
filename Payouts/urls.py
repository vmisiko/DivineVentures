from django.contrib import admin
from django.urls import path
from . import views


app_name = "Payouts"

urlpatterns = [
    
    
    path('pp_callback/', views.Paypal_callback.as_view() , name = "Paypal_callback"), 
    path('how_it_works/', views.HowitWorksView.as_view() , name = "how_it_works"), 
    path('contacts/', views.ContactView.as_view() , name = "contact"),
]