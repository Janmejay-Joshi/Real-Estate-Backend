from rest_framework import serializers
from apps.profiles.models import UserProfileModel

from apps.properties.models import PropertyModel
from rest_flex_fields import FlexFieldsModelSerializer

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserProfileSerializer(FlexFieldsModelSerializer):
    """
    Serves Data For the UserProfileModel
    """

    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = UserProfileModel
        fields = "__all__"
        read_only_fields = (
            "is_prime",
            "is_verified",
            "user",
        )

        expandable_fields = {
            "image": ("apps.properties.ImageSerializer"),
            "user": ("apps.profiles.UserSerializer"),
            "properties": ("apps.properties.PropertySerializer", {"many": True}),
            "wishlist": ("apps.properties.PropertySerializer", {"many": True}),
        }
