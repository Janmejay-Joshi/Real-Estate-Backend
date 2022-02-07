from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.properties.views import PropertyViewSet

router = DefaultRouter()
router.register(r"property", PropertyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
