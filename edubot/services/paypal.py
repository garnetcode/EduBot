"""Imports"""
import base64
import json

import requests
# Create your views here.
from django.core.cache import cache

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

    def __init__(self,payload = None):
        self._headers = None
        self.payload = payload
        self.client_id = "AUiFXuG_L4fI58jrQAZqDTTNJjeIPsN1ozmwiVxREO_jYKRY-BGYJWxTwLw4vdb0MtsWbiHhSQA6J036"
        self.client_secret = "EADMsj2TcCG4sORZUmidFRPgF0J4KbIcJZMjYxAVelvdlXW0F93h_MHJ4XQKblLb4aHSc4z9PLFPZnv8"

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
        self._headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}


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
                    "grant_type":"client_credentials"
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
    
    def create_order(self, payload):
        """Create an order"""
        # amount to be paid to 2 decimal places
        amount = f"{float(payload.get('amount'), 2)}"
        payload = json.dumps(

            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "items": [
                            {
                                "name": payload.get('name').title(),
                                "description": payload.get('description'),
                                "quantity": "1",
                                "unit_amount": {
                                    "currency_code": "USD",
                                    "value": amount
                                }
                            }
                        ],
                        "amount": {
                            "currency_code": "USD",
                            "value": amount,
                            "breakdown": {
                                "item_total": {
                                    "currency_code": "USD",
                                    "value": amount
                                }
                            }
                        }
                    }
                ],
                "application_context": {
                    "return_url": payload.get('returnUrl'),
                    "cancel_url": payload.get('cancelUrl'),
                }
            }
        )


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
        
        self.headers = (PAYPALCLIENTAPI.access_token, False)
        response = requests.post(post_url, data=payload, headers=self.headers)

        if response.status_code == 201:
            response_json = {
                'status': True,
                'paypal_id':response.json().get('id'),
                'url': response.json()['links'][1].get('href')
            }
        else:
            response_json = {
                'status': False,
                'response':response.json()
            }
        return response_json