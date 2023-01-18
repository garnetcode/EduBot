"""Imports and helper functions."""
import re
import requests
from decouple import config


def payment_method(phone_number):
    """Check if phone number is valid."""
    if re.compile(r'26371\d{7}$|071\d{7}$').match(phone_number):
        return "onemoney"
    elif re.compile(r'26373\d{7}$|073\d{7}$').match(phone_number):
        return "telecash"
    else:
        return "ecocash"

def is_phone_number(phone_number):
    """Check if phone number is valid."""
    if re.compile(r'263\d{9}$|0\d{9}$').match(phone_number):
        return True
    else:
        return False

def send_response(response):
    """Send the response."""
    url = f"https://graph.facebook.com/v15.0/{config('Phone_Number_ID')}/messages"
    response = requests.post(
        url=url,
        data=response,
        headers={'Authorization': f'Bearer {config("CLOUD_API_TOKEN")}'}
    )
    print("Response :", response.json())
    return response