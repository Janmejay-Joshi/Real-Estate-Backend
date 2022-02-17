from django.contrib.admin.decorators import action
from django.http.response import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_417_EXPECTATION_FAILED
from rest_framework.views import APIView
from django.conf import settings
from apps.payments.constants import PaymentStatus
from apps.payments.models import Order
from razorpay import Client as RazorPayClient
from razorpay.errors import SignatureVerificationError

# Create your views here.

## History Payment Callbacks

razorpay_client = RazorPayClient(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)

data = {"amount": 500, "currency": "INR", "receipt": "order_rcptid_11"}


class PrimePaymentView(APIView):
    @csrf_exempt
    def post(self, request):
        name = request.data["name"]
        amount = request.data["amount"]
        razorpay_order = razorpay_client.order.create(data)
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return Response(
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/api/pay/callback/",
                "razorpay_key": settings.RAZOR_KEY_ID,
            },
        )


class CallbackView(APIView):
    def post(self, request, format=None):
        def verify_signature(response_data):
            client = RazorPayClient(
                auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
            )
            return client.utility.verify_payment_signature(response_data)

        if "razorpay_signature" in request.data:
            payment_id = request.data["razorpay_payment_id"]
            provider_order_id = request.data["razorpay_order_id"]
            signature_id = request.data["razorpay_signature"]

            order = Order.objects.get(provider_order_id=provider_order_id)
            order.payment_id = payment_id
            order.signature_id = signature_id
            order.save()

            try:
                if verify_signature(request.data):
                    order.status = PaymentStatus.SUCCESS
                    order.save()
                    return Response(status=HTTP_200_OK)
                else:
                    order.status = PaymentStatus.FAILURE
                    order.save()
                    return Response(status=HTTP_417_EXPECTATION_FAILED)
            except SignatureVerificationError:
                return Response(status=HTTP_417_EXPECTATION_FAILED)
