from rest_framework import serializers
from apps.profiles.models import UserProfileModel

from apps.properties.models import PropertyModel


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serves Data For the UserProfileModel
    TODO: Add Expandable Feilds for Image and Properties
    """

    class Meta:
        model = UserProfileModel
        fields = "__all__"
        read_only_fields = ("is_prime",)
