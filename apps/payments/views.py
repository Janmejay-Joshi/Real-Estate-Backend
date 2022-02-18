from datetime import datetime, timedelta, timezone
from django.contrib.admin.decorators import action
from django.http.response import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_208_ALREADY_REPORTED,
    HTTP_417_EXPECTATION_FAILED,
)
from rest_framework.views import APIView
from django.conf import settings
from apps.payments.constants import PaymentStatus
from apps.payments.models import Order
from apps.profiles.models import UserProfileModel
from razorpay import Client as RazorPayClient
from razorpay.errors import SignatureVerificationError
import json

# Create your views here.

## History Payment Callbacks

razorpay_client = RazorPayClient(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)


class PrimePaymentView(APIView):
    @csrf_exempt
    def post(self, request):
        user = UserProfileModel.objects.get(pk=request.data["user"])
        subscription_type = request.data["subscription_type"]

        if (
            (user.prime_status.contact_counter < user.prime_status.counter_limit)
            and (user.prime_status.is_prime)
            and (
                user.prime_status.timestamp
                + timedelta(days=user.prime_status.subscription_period)
                > datetime.now(timezone.utc)
            )
        ):
            return Response(
                {"error": "Already an Valid Prime User"},
                status=HTTP_208_ALREADY_REPORTED,
            )

        if subscription_type == "Basic":
            ammount = 4900
        elif subscription_type == "Pro":
            ammount = 24900
        elif subscription_type == "Premium":
            ammount = 49900
        else:
            return HttpResponseBadRequest

        data = {"amount": ammount, "currency": "INR"}

        razorpay_order = razorpay_client.order.create(data)
        order = Order.objects.create(
            user=user,
            subscription_type=subscription_type,
            provider_order_id=razorpay_order["id"],
        )
        order.save()
        return Response(
            {
                "payment": {
                    "id": razorpay_order["id"],
                    "ammount": 4900,
                }
            },
        )


class CallbackView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        def verify_signature(response_data):
            client = RazorPayClient(
                auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
            )
            return client.utility.verify_payment_signature(response_data)

        data = json.loads(request.data["response"])

        payment_id = data.get("razorpay_payment_id")
        provider_order_id = data.get("razorpay_order_id")
        signature_id = data.get("razorpay_signature")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()

        try:
            if verify_signature(data):
                prime_status = UserProfileModel.objects.get(
                    user__username=order.user,
                ).prime_status

                prime_status.is_prime = True
                prime_status.contact_counter = 0
                prime_status.subscription_type = order.subscription_type

                if order.subscription_type == "Basic":
                    prime_status.counter_limit = 15
                    prime_status.subscription_period = 30
                elif order.subscription_type == "Pro":
                    prime_status.counter_limit = 35
                    prime_status.subscription_period = 60
                elif order.subscription_type == "Premium":
                    prime_status.counter_limit = 99
                    prime_status.subscription_period = 90

                prime_status.save()

                order.status = PaymentStatus.SUCCESS
                order.save()
                return Response(
                    {"status": "SUCCESS"},
                    status=HTTP_200_OK,
                )
            else:
                order.status = PaymentStatus.FAILURE
                order.save()
                return Response(
                    {"status": "FAILURE"},
                    status=HTTP_417_EXPECTATION_FAILED,
                )
        except SignatureVerificationError:
            return Response(
                {"status": "INVALID SIGNATURE"},
                status=HTTP_417_EXPECTATION_FAILED,
            )
