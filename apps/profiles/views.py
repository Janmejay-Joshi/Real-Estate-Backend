from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    AllowAny,
    DjangoObjectPermissions,
    IsAuthenticated,
)
from rest_framework import status

from apps.profiles.models import UserProfileModel
from apps.profiles.serializers import UserProfileSerializer

# Create your views here.


class UserProfileViewSet(GenericViewSet):

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
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, user__username):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
