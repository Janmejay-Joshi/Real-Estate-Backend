from rest_framework import serializers
from apps.profiles.models import UserProfileModel

from apps.properties.models import PropertyModel


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    properties = serializers.SlugRelatedField(
        many=True, queryset=PropertyModel.objects.all(), slug_field="properties"
    )

    wishlist = serializers.SlugRelatedField(
        many=True, queryset=PropertyModel.objects.all(), slug_field="wishlist"
    )

    class Meta:
        model = UserProfileModel
        fields = "__all__"
        read_only_fields = ("user", "username", "is_prime")
