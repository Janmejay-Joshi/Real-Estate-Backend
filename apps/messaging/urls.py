from django.urls import path


from apps.messaging.views import BroadcastOTP, OTPCallback

urlpatterns = [
    path("otp/", BroadcastOTP.as_view()),
    path("otp/callback/", OTPCallback.as_view()),
]
