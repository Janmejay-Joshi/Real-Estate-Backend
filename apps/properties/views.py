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
from apps.properties.models import (
    AmenitiesTags,
    CityModel,
    Image,
    PropertyModel,
    SublocationModel,
)
from apps.properties.serializers import (
    AmenitiesTagsSerializer,
    CitySerializer,
    ImageSerializer,
    PropertySerializer,
)

from apps.profiles.models import Contacted, PrimeModel, UserProfileModel

from django.db.models import F, Q
from rest_flex_fields import FlexFieldsModelViewSet
from datetime import datetime, timedelta, timezone
from twilio.rest import Client
from django.conf import settings

# Create your views here.


class WishUpdateView(APIView):
    def post(self, request, format=None, **kwargs):
        property = get_object_or_404(PropertyModel, pk=request.data["property"])
        profile = get_object_or_404(UserProfileModel, pk=request.data["profile"])

        try:
            if (
                UserProfileModel.objects.get(wishlist__pk=request.data["property"])
                == profile
            ):
                property.wished_by.remove(profile)
                profile.wishlist.remove(property)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                property.wished_by.add(profile)
                profile.wishlist.add(property)
                return Response(status=status.HTTP_201_CREATED)
        except:
            property.wished_by.add(profile)
            profile.wishlist.add(property)
            return Response(status=status.HTTP_201_CREATED)


class ContactedView(APIView):
    def post(self, request, format=None, **kwargs):
        owner = get_object_or_404(UserProfileModel, pk=request.data["owner"])
        buyer = get_object_or_404(UserProfileModel, pk=request.data["buyer"])
        property = get_object_or_404(PropertyModel, pk=request.data["property"])

        if (
            (buyer.prime_status.contact_counter < buyer.prime_status.counter_limit)
            and (buyer.prime_status.is_prime)
            and (
                buyer.prime_status.timestamp
                + timedelta(days=buyer.prime_status.subscription_period)
                > datetime.now(timezone.utc)
            )
        ):
            if not (Contacted.objects.filter(user=buyer, property=property)):
                contact_owner = Contacted.objects.create(user=buyer, property=property)
                contact_buyer = Contacted.objects.create(user=owner, property=property)

                owner.contacted_by.add(contact_owner)

                buyer.contacted_to.add(contact_buyer)
                buyer_prime = PrimeModel.objects.get(pk=buyer.prime_status.id)
                buyer_prime.contact_counter += 1
                buyer_prime.save()

                owner.save()
                buyer.save()

                message_to_broadcast = f"""
                        Hi {owner.user.first_name},
                        {buyer.user.first_name} {buyer.user.last_name} has just contacted you and wants to know about {property.property_name}.
                        Connect now & keep checking the My Responses section on reessol.com for more contacts"
                    """
                print(message_to_broadcast)

                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                recipient = "+91" + request.data[owner.mobile]
                if recipient:
                    client.messages.create(
                        to=recipient,
                        from_=settings.TWILIO_NUMBER,
                        body=message_to_broadcast,
                    )

                return Response(
                    {"response": "Sucessfully Added"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Already Contacted"},
                    status=status.HTTP_208_ALREADY_REPORTED,
                )
        else:
            return Response(
                {"error": "Prime Expired"},
                status=status.HTTP_417_EXPECTATION_FAILED,
            )


class ImageViewSet(FlexFieldsModelViewSet):
    """
    Create, update fetch or destroy an (Image) instance
    url: /api/image/ , /api/image/<int:pk>
    actions: [GET, POST, PUT, PATCH, DELETE]
    """

    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class CityViewSet(FlexFieldsModelViewSet):
    """
    Create, update fetch or destroy an (Image) instance
    url: /api/image/ , /api/image/<int:pk>
    actions: [GET, POST, PUT, PATCH, DELETE]
    """

    serializer_class = CitySerializer
    queryset = CityModel.objects.all()
    lookup_field = "city"


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
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        owner = get_object_or_404(UserProfileModel, pk=request.data["posted_by"])
        owner.properties.add(serializer.data["id"])
        owner.save()

        try:
            location = SublocationModel.objects.get(location=request.data["location"])

        except:
            location = SublocationModel.objects.create(
                location=request.data["location"]
            )

        try:
            city = CityModel.objects.get(city=request.data["city"])
        except:
            city = CityModel.objects.create(city=request.data["city"])

        city.sublocations.add(location)
        city.save()

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

    def destroy(self, request, pk):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        property_name = self.request.query_params.get("property_name")
        prime = self.request.query_params.get("prime")
        furnishing = self.request.query_params.get("furnishing")
        possession = self.request.query_params.get("possession")
        for_status = self.request.query_params.get("for")
        up_limit = self.request.query_params.get("max")
        low_limit = self.request.query_params.get("min")
        low_area_limit = self.request.query_params.get("minarea")
        up_area_limit = self.request.query_params.get("maxarea")
        bathroom = self.request.query_params.get("bathrooms")
        bedroom = self.request.query_params.get("bedrooms")
        availability = self.request.query_params.get("availability")
        posted_by = self.request.query_params.get("posted_by")
        popular = self.request.query_params.get("popular")
        featured = self.request.query_params.get("featured")
        location = self.request.query_params.get("location")
        sublocality = self.request.query_params.get("sublocality")
        floor = self.request.query_params.get("floor")
        corner = self.request.query_params.get("corner")
        gated = self.request.query_params.get("gated")
        prime_order = self.request.query_params.get("prime_order")
        agent_order = self.request.query_params.get("agent_order")
        latest = self.request.query_params.get("latest")

        if property_name is not None:
            queryset = queryset.filter(property_name=property_name)
        if posted_by is not None:
            queryset = queryset.filter(posted_by=posted_by)
        if city is not None:
            queryset = queryset.filter(city=city)
        if agent_order is not None:
            queryset = queryset.filter(posted_by__city=agent_order)
            queryset = queryset.order_by("posted_by__user_type")
        if prime is not None:
            queryset = queryset.filter(prime_property=prime)
        if sublocality is not None:
            queryset = queryset.filter(sublocality=sublocality)
        if type is not None:
            queryset = queryset.filter(property_type=type)
        if floor is not None:
            filter = Q()
            floor = floor.split(",")
            for filter_q in floor:
                filter = filter | Q(floor=floor)
            queryset = queryset.filter(filter)
        if furnishing is not None:
            filter = Q()
            furnishing = furnishing.split(",")
            for filter_q in furnishing:
                filter = filter | Q(furnishing_status=filter_q)
            queryset = queryset.filter(filter)
        if low_limit is not None:
            queryset = queryset.filter(price__gte=low_limit)
        if up_limit is not None:
            queryset = queryset.filter(price__lte=up_limit)
        if low_area_limit is not None:
            queryset = queryset.filter(property_size__gte=low_area_limit)
        if up_area_limit is not None:
            queryset = queryset.filter(property_size__lte=up_area_limit)
        if bathroom is not None:
            filter = Q()
            bathroom = bathroom.split(",")
            for bathroom_q in bathroom:
                filter = filter | Q(bathrooms=bathroom_q)
            queryset = queryset.filter(filter)
        if bedroom is not None:
            filter = Q()
            bedroom = bedroom.split(",")
            for filter_q in bedroom:
                filter = filter | Q(bedrooms=filter_q)
            queryset = queryset.filter(filter)
        if location is not None:
            filter = Q()
            location = location.split(",")
            print(location)
            for filter_q in location:
                filter = filter | Q(location=filter_q)
            queryset = queryset.filter(filter)
            print(queryset)
        if availability is not None:
            queryset = queryset.filter(availability=availability)
        if corner is not None:
            queryset = queryset.filter(corner=corner)
        if gated is not None:
            queryset = queryset.filter(gated=gated)
        if possession is not None:
            queryset = queryset.filter(possession=possession)
        if for_status is not None:
            queryset = queryset.filter(for_status=for_status)
        if popular:
            queryset = queryset.order_by("-visits")
        if latest:
            queryset = queryset.order_by("-timestamp")
        if featured:
            queryset = queryset.order_by("-prime_property")
        if prime_order:
            queryset = queryset.order_by("-posted_by__prime_status__is_prime")
            queryset = queryset.order_by("posted_by__user_type")

        return queryset


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

    def destroy(self, request, pk):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
