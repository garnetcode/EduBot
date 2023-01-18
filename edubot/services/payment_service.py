"""Imports"""
import hashlib
import requests
from django.conf import settings


class ProcessPayment(object):
    """Process Customer payment"""

    def __init__(
        self, paying_phone_number, amount, method, reference, authemail
    ) -> str:
        self.phone = paying_phone_number
        self.reference = reference
        self.amount = amount
        self.method = method
        self.authemail = authemail

    def clean_response(self, response_data):
        """Clean response"""
        print("CLEANING RESPONSE DATA : ", response_data)
        response_ = response_data.decode("utf-8").split("&")
        response_ = {
            item.split("=")[0]: item.split("=")[1]
            .replace("%3a", ":")
            .replace("%2f", "/")
            .replace("%3f", "?")
            .replace("%3d", "=")
            .replace("+", " ")
            for item in response_
        }
        return response_

    def process(self):
        """Process Payment!"""

        data = {
            "id": settings.PAYNOW_INTEGRATION_ID,
            "reference": self.reference,
            "amount": float(self.amount),
            "phone": self.phone,
            "method": self.method,
            "authemail": self.authemail,
            "returnurl": f"{settings.NGROK}/api/v1/poll/{self.reference}",
            "resulturl": f"{settings.NGROK}/webhook/",
            "status": "Message",
        }
        print("PAYMENT DATA : ", data)

        hash_data = list([str(i) for i in data.values()])
        hash_data.append(settings.PAYNOW_INTEGRATION_KEY)
        data["hash"] = (
            hashlib.sha512("".join(hash_data).encode("utf-8")).hexdigest().upper()
        )
        response_data = requests.post(
            url="https://www.paynow.co.zw/interface/remotetransaction", data=data
        )
        if response_data.status_code == 200:
            response_ = self.clean_response(response_data.content)
            print('SECONDARY : ',response_)
            if response_.get("status") == "Ok":
                hash_ = response_.pop("hash")
                hash_data = list([str(i) for i in response_.values()])
                hash_data.append(settings.PAYNOW_INTEGRATION_KEY)
                passed_integrity_check = (
                    hashlib.sha512("".join(hash_data).encode("utf-8"))
                    .hexdigest()
                    .upper()
                    == hash_
                )
                print("INTEGRITY CHECK PASS: ", passed_integrity_check)
                if passed_integrity_check:
                    return response_
                return {"status": "Failed integrity check!"}

        else:
            response_ = {"status": "Error", "message": "Failed to process payment!"}
        return response_

    def poll(self, url=None):
        """Poll for status"""
        if url:
            results = requests.get(url=url)
            if results.status_code == 200:
                return self.clean_response(results.content)
        return None
