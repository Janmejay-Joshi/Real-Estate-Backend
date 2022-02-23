from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.properties.views import (
    AmenitiesTagsViewSets,
    CityViewSet,
    ContactedView,
    ImageViewSet,
    PropertyFilter,
    PropertyViewSet,
    WishUpdateView,
)

router = DefaultRouter()
router.register(r"property", PropertyViewSet)
router.register(r"tags/amenities", AmenitiesTagsViewSets)
router.register(r"image", ImageViewSet)
router.register(r"city", CityViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("filter", PropertyFilter.as_view()),
    path("wish", WishUpdateView.as_view()),
    path("contact", ContactedView.as_view()),
]
