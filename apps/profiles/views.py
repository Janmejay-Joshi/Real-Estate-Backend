from django.contrib.auth.models import User
from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    AllowAny,
    DjangoObjectPermissions,
    IsAuthenticated,
)
from rest_framework import generics, status

from apps.profiles.models import UserProfileModel
from apps.profiles.serializers import UserProfileSerializer

# Create your views here.


class UserFilter(generics.ListAPIView):
    """
    Fetch all (Property) instance with filters provided in the params
    url: /api/filter
    example: /api/filter?city=indore&prime=True
    actions: [GET]
    """

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = UserProfileModel.objects.all()
        agent_order = self.request.query_params.get("agent_order")

        if agent_order is not None:
            queryset = queryset.filter(city=agent_order)
            queryset = queryset.filter(user_type="Agent")
            queryset = queryset.order_by("prime_status__is_prime")

        return queryset


class UserProfileUsernameViewSet(FlexFieldsModelViewSet):

    """
    Create, update fetch or destroy an (UserProfile) instance
    url: /api/profile/ , /api/profile/<string:username>
    actions: [GET, POST, PUT, PATCH, DELETE]
    """

    serializer_class = UserProfileSerializer
    queryset = UserProfileModel.objects.all()
    permission_classes = [DjangoObjectPermissions]
    lookup_field = "user__username"

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ("list", "create", "retrieve", "update", "partial_update"):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # return self.get_paginated_response(self.paginate_queryset(serializer.data))
        return Response(serializer.data)

    def retrieve(self, request, user__username):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, user__username):
        user = self.get_object()
        django_user = User.objects.get(username=user__username)
        django_user.first_name = request.data["first_name"]
        django_user.last_name = request.data["last_name"]
        django_user.save()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, user__username):
        user = self.get_object()
        django_user = User.objects.get(username=user__username)
        django_user.first_name = request.data["first_name"]
        django_user.last_name = request.data["last_name"]
        django_user.save()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, user__username):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileViewSet(FlexFieldsModelViewSet):

    """
    Create, update fetch or destroy an (UserProfile) instance
    url: /api/profile/ , /api/profile/<string:username>
    actions: [GET, POST, PUT, PATCH, DELETE]
    """

    serializer_class = UserProfileSerializer
    queryset = UserProfileModel.objects.all()
    permission_classes = [DjangoObjectPermissions]
    lookup_field = "mobile"

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ("list", "create", "retrieve", "update", "partial_update"):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # return self.get_paginated_response(self.paginate_queryset(serializer.data))
        return Response(serializer.data)

    def retrieve(self, request, mobile):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, mobile):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, mobile):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, mobile):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
