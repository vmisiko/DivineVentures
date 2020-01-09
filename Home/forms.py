from django import forms
from django.forms import ModelForm
# from .models import 


class Mpesa_checkout(forms.Form):
    
     phone_number = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':"2547xxxxxxxxx  "}))
    
class Mpesa_c2b_checkout(forms.Form):

    mpesa_code = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':" i.e MNxxxxx "}))


class Mpesa_withwraw(forms.Form):
    
    first_name = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':" Enter your first name  "}))
    
    last_name = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':"Enter your last name  "}))

    phone_number = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':"Enter a registered phone bumber  "}))
    
    email = forms.CharField(widget = forms.TextInput(attrs = {
        "placeholder": "Enter a valid email adress"
    }))

class Paypal_withdraw(forms.Form):
    
    f_name = forms.CharField(label = "First Name", widget = forms.TextInput(attrs = {
    'placeholder':" Enter your first name  "}))
    
    l_name = forms.CharField( label = "Last Name",widget = forms.TextInput(attrs = {
    'placeholder':"Enter your last name  "}))

    p_number = forms.CharField( label = "Phone Number",widget = forms.TextInput(attrs = {
    'placeholder':"Enter your phone bumber  "}))
    
    p_email = forms.CharField(label = "Paypal Email",widget = forms.TextInput(attrs = {
        "placeholder": "Enter paypal email adress"
    }))

    # class Meta:
        
    #     labels = {
    #         "l_name": "Last_name",
    #         "f_name" : "first_name",
    #         "p_number": "phone_number",
    #         "p_email": "paypal_email"
    #     }
        