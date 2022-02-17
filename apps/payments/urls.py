from django.urls import path

from apps.payments.views import CallbackView, PrimePaymentView


urlpatterns = [
    path("pay/", PrimePaymentView.as_view()),
    path("pay/callback/", CallbackView.as_view()),
]
