from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.permissions import (
    AllowAny,
    DjangoObjectPermissions,
    IsAuthenticated,
)
from rest_framework import status
from apps.properties.models import AmenitiesTags, FeaturesTags, Image, PropertyModel
from apps.properties.serializers import (
    AmenitiesTagsSerializer,
    FeaturesTagsSerializer,
    ImageSerializer,
    PropertySerializer,
)

from apps.profiles.models import UserProfileModel

from django.db.models import F
from rest_flex_fields import FlexFieldsModelViewSet

# Create your views here.


class WishUpdateView(APIView):
    def post(self, request, format=None, **kwargs):
        user = get_object_or_404(User, pk=request.data["user"])
        property = get_object_or_404(PropertyModel, pk=request.data["property"])
        profile = get_object_or_404(UserProfileModel, pk=request.data["profile"])

        property.wished_by.add(user)
        profile.wishlist(property)


class ImageViewSet(FlexFieldsModelViewSet):
    """
    Create, update fetch or destroy an (Image) instance
    url: /api/image/ , /api/image/<int:pk>
    actions: [GET, POST, PUT, PATCH, DELETE]
    """

    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class PropertyViewSet(GenericViewSet):
    """
    Create, update fetch or destroy an (Property) instance
    url: /api/property/ , /api/property/<int:pk>
    actions: [GET, POST, PUT, PATCH, DELETE]
    """

    serializer_class = PropertySerializer
    queryset = PropertyModel.objects.all()
    permission_classes = [DjangoObjectPermissions]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ("list", "retrieve", "create"):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # return self.get_paginated_response(self.paginate_queryset(serializer.data))
        return Response(serializer.data)

    def retrieve(self, request, pk):
        item = self.get_object()
        PropertyModel.objects.filter(pk=pk).update(visits=F("visits") + 1)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def update(self, request, pk):
        property = self.get_object()
        serializer = self.get_serializer(property, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        property = self.get_object()
        serializer = self.get_serializer(property, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    ## City Name Type


class PropertyFilter(generics.ListAPIView):
    """
    Fetch all (Property) instance with filters provided in the params
    url: /api/filter
    example: /api/filter?city=indore&prime=True
    actions: [GET]
    """

    serializer_class = PropertySerializer

    def get_queryset(self):
        queryset = PropertyModel.objects.all()
        city = self.request.query_params.get("city")
        type = self.request.query_params.get("type")
        property_name = self.request.query_params.get("name")
        prime = self.request.query_params.get("prime")
        furnishing = self.request.query_params.get("furnishing")
        possession = self.request.query_params.get("possession")
        for_status = self.request.query_params.get("for")
        up_limit = self.request.query_params.get("max")
        low_limit = self.request.query_params.get("min")
        bathroom = self.request.query_params.get("bathroom")
        bedroom = self.request.query_params.get("bedroom")
        availability = self.request.query_params.get("availability")

        if property_name is not None:
            queryset = queryset.filter(property_name=property_name)
        if city is not None:
            queryset = queryset.filter(city=city)
        if prime is not None:
            queryset = queryset.filter(prime_property=prime)
        if type is not None:
            queryset = queryset.filter(property_type=type)
        if furnishing is not None:
            queryset = queryset.filter(furnishing_status=furnishing)
        if low_limit is not None:
            queryset = queryset.filter(price__gte=low_limit)
        if up_limit is not None:
            queryset = queryset.filter(price__lte=up_limit)
        if bathroom is not None:
            queryset = queryset.filter(bathroom=bathroom)
        if bedroom is not None:
            queryset = queryset.filter(bedroom=bedroom)
        if availability is not None:
            queryset = queryset.filter(availability=availability)
        if possession is not None:
            queryset = queryset.filter(possession=possession)
        if for_status is not None:
            queryset = queryset.filter(for_status=for_status)
        return queryset


class FeaturesTagsViewSets(GenericViewSet):

    """
    Create, update fetch or destroy an (Feture Tag) instance
    url: /api/tags/features/ , /api/tags/features/<int:pk>/
    actions: [GET, POST, DELETE]
    """

    serializer_class = FeaturesTagsSerializer
    queryset = FeaturesTags.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # return self.get_paginated_response(self.paginate_queryset(serializer.data))
        return Response(serializer.data)

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AmenitiesTagsViewSets(GenericViewSet):

    """
    Create, update fetch or destroy an (Amenities Tag) instance
    url: /api/tags/amenities/ , /api/tags/amenities/<int:pk>/
    actions: [GET, POST, DELETE]
    """

    serializer_class = AmenitiesTagsSerializer
    queryset = AmenitiesTags.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # return self.get_paginated_response(self.paginate_queryset(serializer.data))
        return Response(serializer.data)

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
