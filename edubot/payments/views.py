"""Views for payments app."""
import json
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
#pylint: disable=import-error
#pylint: disable=no-name-in-module
from utils.helper_functions import send_response
from payments.models import Payment
from payments.serializers import PaymentSerializer
from users.permissions import IsStaff

class PaymentsWebHook(APIView):
    """Payments Webhook"""

    permission_classes = []

    @csrf_exempt
    def post(self, request):
        """Payments Webhook"""
        payment_confirmation = request.data
        print("***WEBHOOK :: ", payment_confirmation)
        reference = payment_confirmation.get("reference")

        status = payment_confirmation.get("status")#
        #pylint: disable=no-member
        if status == "Paid":

            #pylint: disable=no-member
            payment = Payment.objects.get(reference=reference)

            ##########################################
            # Enroll user in course                  #
            ##########################################
            payment.user.enrolled_courses.add(payment.course)
            payment.course.students.add(payment.user)
            payment.user.save()
            payment.course.save()

            receipt_like_template = f"""
                *EduBot ✅*\n\nThank you for subscribing to *{payment.course.name}*.\n\nYour payment of *$ {payment.package.price}* has been received.\n\nIf you have any questions regarding your payment, please contact us at \n\n*[admin@edubot.com]* \n\nor call \n\n*[263771516726]*
            """
            receipt ={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": payment.user.phone_number,
                "type": "interactive",
                "interactive": json.dumps({
                    "type": "button",
                    "body": {
                        "text": receipt_like_template
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "menu",
                                    "title": "🏠 Menu"
                                }
                            }
                        ]
                    }
                })
            }
        elif status == "Awaiting Delivery":
            payment = Payment.objects.get(reference=reference)
            receipt_like_template = f"""
                *EduBot ✅*\n\nThank you for subscribing to {payment.course.name}.\n\nYour payment of ${payment.package.price} with payment id {payment.id} is being processed and will be delivered shortly.\n\nIf you have any questions regarding your payment, please contact us at  \n\n*[admin@edubot.com]* \n\nor call \n\n*[263771516726]*
                """
            receipt ={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": payment.user.phone_number,
                "type": "interactive",
                "interactive": json.dumps({
                    "type": "button",
                    "body": {
                        "text": receipt_like_template
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "menu",
                                    "title": "🏠 Menu"
                                }
                            }
                        ]
                    }
                })
            }
        elif status == "Error":
            payment = Payment.objects.get(reference=reference)
            receipt ={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": payment.user.phone_number,
                "type": "interactive",
                "interactive": json.dumps({
                    "type": "button",
                    "body": {
                        "text": f"*EduBot❌*\n\nWe cannot process your payment of ${payment.package.price} for {payment.course.name} at the moment. Please try again later."
                    },
                    "action": {
                        "buttons": [
                            
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "menu",
                                    "title": "🏠 Menu"
                                }
                            }
                        ]
                    }
                })
            }
        else:
            payment = Payment.objects.get(reference=reference)
            receipt ={
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": payment.user.phone_number,
                "type": "interactive",
                "interactive": json.dumps({
                    "type": "button",
                    "body": {
                        "text": f"*EduBot❌*\n\nYour payment of ${payment.package.price} for {payment.course.name}  {'was cancelled' if status == 'Cancelled' else 'failed'}.\n\nIf you did not cancel cancel it, you might not have sufficient balance. Please check your balance & press retry to try again or enter a different phone number to pay with."
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": cache.get(payment.user.phone_number).get("data").get("payee") if cache.get(payment.user.phone_number) else "retry",
                                    "title": "🔄 Retry"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "menu",
                                    "title": "🏠 Menu"
                                }
                            }
                        ]
                    }
                })
            }
        print("Declined :: ", Payment.objects.get(reference=reference).payment_status )
        if payment.payment_status and Payment.objects.get(reference=reference).payment_status != "Declined":
            send_response(response=receipt)  
        Payment.objects.filter(reference=reference).update(
            **{
                "payment_status": status.capitalize(),
                "is_paid": True if status in ["Paid", "Awaiting Delivery"] else False,
            }
        )    
        return JsonResponse({}, status=200)


class PaymentViewSet(ModelViewSet):
    """Payments"""

    serializer_class = PaymentSerializer
    #pylint: disable=no-member
    queryset = Payment.objects.all()
    permission_classes = [IsStaff, ]

    def get_queryset(self):
        """Get queryset"""
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create payment"""
        # Create payment not allowed
        return JsonResponse({}, status=405)


    def destroy(self, request, *args, **kwargs):
        """Delete payment"""
        # Delete payment not allowed
        return JsonResponse({}, status=405)

