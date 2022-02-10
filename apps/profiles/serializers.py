from rest_framework import serializers
from apps.profiles.models import UserProfileModel

from apps.properties.models import PropertyModel
from rest_flex_fields import FlexFieldsModelSerializer


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
            "user",
        )

        expandable_fields = {
            "image": ("apps.properties.ImageSerializer"),
            "properties": ("apps.properties.PropertySerializer", {"many": True}),
            "wishlist": ("apps.properties.PropertySerializer", {"many": True}),
        }
