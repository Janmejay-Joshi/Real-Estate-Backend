from django.urls import path, include
from rest_framework import routers
from apps.profiles.views import UserProfileUsernameViewSet, UserProfileViewSet


router = routers.DefaultRouter()
router.register(r"profile", UserProfileViewSet)
router.register(r"profile_name", UserProfileUsernameViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
