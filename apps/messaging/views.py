from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView
from twilio.rest import Client
from random import randint

from apps.messaging.models import OTPModel
from apps.profiles.models import UserProfileModel

# Create your views here.


def randomOTPGenerate():
    return randint(100, 999)


class BroadcastOTP(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        otp_object = OTPModel.objects.get(user=request.data["user"])
        otp_object.otp = randomOTPGenerate()
        otp_object.save()

        message_to_broadcast = f"Your 9Roof Login OTP is {otp_object.otp}"

        print(message_to_broadcast)

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        recipient = request.data["phone"]
        if recipient:
            client.messages.create(
                to=recipient, from_=settings.TWILIO_NUMBER, body=message_to_broadcast
            )
        return Response({"response": "messages sent!"}, status=HTTP_200_OK)


class OTPCallback(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        otp_object = OTPModel.objects.get(user=request.data["user"])
        if otp_object.otp == request.data["OTP"]:
            user = UserProfileModel.objects.get(user=request.data["user"])
            user.is_verified = True
            user.save()

            otp_object.otp = None
            otp_object.save()

            return Response({"response": "Account Verified"}, status=HTTP_200_OK)

        otp_object.otp = None
        otp_object.save()
        return Response({"response": "Invalid OTP"}, status=HTTP_406_NOT_ACCEPTABLE)
