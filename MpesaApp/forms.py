from django import forms
from django.forms import ModelForm
# from .models import 


class Mpesa_checkout(forms.Form):
    
     phone_number = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':"2547xxxxxxxxx  "}))
    
class Mpesa_c2b_checkout(forms.Form):

    mpesa_code = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':" i.e MNxxxxx "}))





    