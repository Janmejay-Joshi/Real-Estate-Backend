from django.urls import path, include
from rest_framework import routers
from apps.profiles.views import UserProfileViewSet


router = routers.DefaultRouter()
router.register(r"profile", UserProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
