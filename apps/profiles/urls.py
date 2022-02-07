from django.urls import path, include
from rest_framework import routers

from apps.profiles.views import BuyerUserViewSet, AgentUserViewSet, SellerUserViewSet

router = routers.DefaultRouter()
router.register(r"buyer", BuyerUserViewSet)
router.register(r"agent", AgentUserViewSet)
router.register(r"seller", SellerUserViewSet)

urlpatterns = [
    path("profile/", include(router.urls)),
]
