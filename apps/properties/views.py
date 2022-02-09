from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import (
    AllowAny,
    DjangoObjectPermissions,
    IsAuthenticated,
)
from rest_framework import status
from apps.properties.models import AmenitiesTags, FeaturesTags, PropertyModel
from apps.properties.serializers import (
    AmenitiesTagsSerializer,
    FeaturesTagsSerializer,
    PropertySerializer,
)

from django.db.models import F

# Create your views here.


class PropertyViewSet(GenericViewSet):
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

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    ## City Name Type


class PropertyFilter(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = PropertyModel.objects.all()
        city = self.request.query_params.get("city")
        type = self.request.query_params.get("type")
        property_name = self.request.query_params.get("name")
        prime = self.request.query_params.get("prime")
        furnishing = self.request.query_params.get("furnishing")
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
        return queryset


class FeaturesTagsViewSets(GenericViewSet):
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
