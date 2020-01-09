import base64
import requests
from divineVentures.mpesa import keys
from datetime import datetime
from divineVentures.mpesa.access_token import generate_access_token
from divineVentures.mpesa.encode import generate_password
from divineVentures.mpesa.utils import formatted_time

# print(datetime.now())2019-10-23 19:35:31.462259
# 2019-10-23 19:35:31.462259 = 





def lipa_na_mpesa(phone_number, amount , callbackurl, AccountReference,):
    phone = phone_number
    account = AccountReference  
    callbackurl = callbackurl
    formated_time = formatted_time()

    # print(formated_time, " this is formatted time")

    decoded_password = generate_password(formated_time) 
    # print(decoded_password, " this is decoded password")
    

    my_access_token = generate_access_token()
    # print(my_access_token, " this is my access token")

    
    access_token = my_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer %s" % access_token }

    request = {

        "BusinessShortCode": keys.bussiness_shortcode,
        "Password": decoded_password,
        "Timestamp": formated_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": phone,
        "PartyB": keys.bussiness_shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callbackurl,
        "AccountReference": account,
        "TransactionDesc": "pay for fees",

      }
      
    response = requests.post(api_url, json = request, headers=headers)
      
    print (response.text)

    return response.json

# lipa_na_mpesa(phone_number = "0721649416", amount = "23", AccountReference = "1234556")