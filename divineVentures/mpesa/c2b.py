import requests

from divineVentures.mpesa.access_token import generate_access_token
from divineVentures.mpesa import keys

def register_url():

    access_token = generate_access_token()
    api_url = "http://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = { "ShortCode": keys.short_code,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://5d8786c6.ngrok.io",
        "ValidationURL": "https://5d8786c6.ngrok.io/nlm"}
    
    response = requests.post(api_url, json = request, headers=headers)
    
    print (response.text)
    

register_url()

# def c2b_simulation():

#     access_token = generate_access_token()
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
#     headers = {"Authorization": "Bearer %s" % access_token}
#     request = { 
#         "ShortCode": keys.short_code,
#         "CommandID": "CustomerPayBillOnline",
#         "Amount": "100",
#         "Msisdn": keys.mssisdn,
#         "BillRefNumber": "account"

#         }
    
#     response = requests.post(api_url, json = request, headers=headers)
    
#     print (response.text)