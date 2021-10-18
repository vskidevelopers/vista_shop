import requests
import json

import base64
from datetime import datetime

import keys
# from . import keys
# from .keys import consumer_key, consumer_secret, phone_number, shodecode,business_short_code, lipa_na_mpesa_passkey
from requests.auth import HTTPBasicAuth

unformatted_time = datetime.now()
formatted_time = unformatted_time.strftime("%Y%m%d%H%M%S")
print(unformatted_time, "This is the unformatted time")
print(formatted_time, "This is the formatted time")


data_to_encode = keys.business_short_code + keys.lipa_na_mpesa_passkey + formatted_time
encoded_data = base64.b64encode(data_to_encode.encode())

decoded_password = encoded_data.decode("utf-8")
print("decoded_password", decoded_password)

consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

r = requests.get(api_URL, auth=HTTPBasicAuth(
    consumer_key, consumer_secret))

json_response = r.json()
# json_response = json.loads(r.text)
print(json_response)
print("json:", json_response)
my_access_token = json_response['access_token']


def lipa_na_mpesa():
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": keys.business_short_code,
        "Password": decoded_password,
        "Timestamp": formatted_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "50",
        "PartyA": keys.phone_number,
        "PartyB": keys.business_short_code,
        "PhoneNumber": keys.phone_number,
        "CallBackURL": "https://vistavideos.com/lipanampesa",
        "AccountReference": "mamushka",
        "TransactionDesc": "Pay Goods",
    }
    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


lipa_na_mpesa()
