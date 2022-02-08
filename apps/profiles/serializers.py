from rest_framework import serializers
from apps.profiles.models import UserProfileModel

from apps.properties.models import PropertyModel


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = "__all__"
        read_only_fields = ("is_prime",)
