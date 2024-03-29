from rest_framework import serializers
from apps.profiles.models import Contacted, PrimeModel, UserProfileModel

from rest_flex_fields import FlexFieldsModelSerializer

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimeModel
        fields = "__all__"


class ContactedSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Contacted
        fields = "__all__"

        expandable_fields = {
            "user": ("apps.profiles.UserProfileSerializer"),
            "property": ("apps.properties.PropertySerializer"),
        }


class UserProfileSerializer(FlexFieldsModelSerializer):
    """
    Serves Data For the UserProfileModel
    """

    username = serializers.ReadOnlyField(source="user.username")
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")

    class Meta:
        model = UserProfileModel
        fields = "__all__"
        read_only_fields = (
            "prime_status",
            "is_verified",
            "user",
        )

        expandable_fields = {
            "image": ("apps.properties.ImageSerializer"),
            "user": ("apps.profiles.UserSerializer"),
            "prime_status": ("apps.profiles.PrimeSerializer"),
            "properties": ("apps.properties.PropertySerializer", {"many": True}),
            "wishlist": ("apps.properties.PropertySerializer", {"many": True}),
            "contacted_by": ("apps.profiles.ContactedSerializer", {"many": True}),
            "contacted_to": ("apps.profiles.ContactedSerializer", {"many": True}),
        }
