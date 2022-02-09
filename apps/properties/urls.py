from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.properties.views import (
    AmenitiesTagsViewSets,
    FeaturesTagsViewSets,
    PropertyFilter,
    PropertyViewSet,
)

router = DefaultRouter()
router.register(r"property", PropertyViewSet)
router.register(r"tags/features", FeaturesTagsViewSets)
router.register(r"tags/amenities", AmenitiesTagsViewSets)

urlpatterns = [
    path("", include(router.urls)),
    path("filter", PropertyFilter.as_view()),
]
