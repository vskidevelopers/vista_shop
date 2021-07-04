import requests
from requests.auth import HTTPBasicAuth

import keys

consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

r = requests.get(api_URL, auth=HTTPBasicAuth(
    consumer_key, consumer_secret))

json_response = r.json()

my_access_token = json_response['access_token']


def register_url():
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

    headers = {"Authorization": "Bearer %s" % my_access_token}
    request = {
        "ShortCode": keys.shodecode,
        "ResponseType": "Complete",
        "ConfirmationURL": "https://vistavideos.com/confirmation",
        "ValidationURL": "https://vistavideos.com/validation_url"}

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


register_url()
