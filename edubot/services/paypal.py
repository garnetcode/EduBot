"""Imports"""
import base64
import json

import requests
# Create your views here.
from django.core.cache import cache
from decouple import config


def get_jwt_tokens(platform):
    """
    Gets and returns JWT tokens from cache
    """
    try:
        return cache.get(f"{platform}_access_token")
    except KeyError:
        return None


class PAYPALCLIENTAPI:
    """
    Class used to represent the Paypal API.
    Attributes
    ----------
    headers : str
        HTTP Headers for the requests
    PAYPAL_BASE_URL : str
        api server base url for requests
    acess_token : str
        jwt access token
    refresh_token : str
        jwt refresh token
    Methods
    -------
    login()
        Performs login to get new tokens
    """

    # PAYPAL_BASE_URL = settings.PAYPAL_BASE_URL
    access_token = get_jwt_tokens('paypal')

    def __init__(self, payload=None):
        self._headers = None
        self.payload = payload
        self.client_id = config('PAYPAL_CLIENT_ID')
        self.client_secret = config('PAYPAL_CLIENT_SECRET')

    @property
    def headers(self):
        """Gets HTTP headers for the request"""
        print('getting headers')
        return self._headers

    @headers.setter
    def headers(self, token):
        """Sets HTTP headers for the request"""
        print('setting header')
        token = cache.get('paypal_access_token')
        if token is None:
            access_token = PAYPALCLIENTAPI.login(
                self.client_id,
                self.client_secret
            )
        else:
            access_token = token
        self._headers = {'Authorization': f'Bearer {access_token}',
                         'Content-Type': 'application/json'}

    @staticmethod
    def login(client_id, client_secret):
        """Logs in to get new tokens"""
        print('login in')
        auth_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token?grant_type=client_credentials"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode()).decode()}"
        }
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(auth_url, data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            access_token = data['access_token']
            cache.set(
                'paypal_access_token',
                access_token,
                timeout=3600*24
            )
            return access_token
        else:
            return ''

    def capture(self, payment_id):
        """Create an order"""
        
        post_url = f"https://api.sandbox.paypal.com/v2/checkout/orders/{payment_id}/capture"
        self.headers = (PAYPALCLIENTAPI.access_token, False)
        response = requests.post(post_url, headers=self.headers)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {
                'error': response.content
            }



    def online_payment(self):
        """Makes an online payment"""
        print('making online payment')
        post_url = "https://api.sandbox.paypal.com/v2/checkout/orders"
        payload = json.dumps({
            "intent": "CAPTURE",
            "application_context": {
                "return_url": self.payload.get('returnUrl'),
                "cancel_url": self.payload.get('cancelUrl'),
                "brand_name": self.payload.get('brandName'),
                "landing_page": "BILLING",
                "user_action": "CONTINUE"
            },
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": self.payload.get('currency'),
                        "value": self.payload.get('amount')
                    }
                }
            ]
        })
        print('payload', payload)

        self.headers = (PAYPALCLIENTAPI.access_token, False)
        response = requests.post(post_url, data=payload, headers=self.headers)
        print("PayPal Response : ", response.json())

        if response.status_code == 201:
            response = response.json()
            response_json = {
                'successful': True,
                'paypal_id': response.get('id'),
                'status': "Created",
                'url': response['links'][1].get('href'),
                'response': response
            }
        else:
            response_json = {
                'successful': False,
                'response': response.json()
            }
        return response_json
