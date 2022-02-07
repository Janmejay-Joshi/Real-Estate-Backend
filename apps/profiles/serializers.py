from rest_framework import serializers

from apps.profiles.models import AgentUserProfile, BuyerUserProfile, SellerUserProfile
from apps.properties.models import PropertyModel


class BuyerUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = BuyerUserProfile
        fields = (
            "id",
            "username",
            "email",
            "user_type",
            "bio",
            "mobile",
            "address",
            "location",
            "pincode",
            "wishlist",
        )

        read_only_fields = (
            "username",
            "user_type",
        )


class SellerUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.CharField(source="user.email")
    properties = serializers.SlugRelatedField(
        many=True, queryset=PropertyModel.objects.all(), slug_field="text"
    )

    class Meta:
        model = SellerUserProfile
        fields = (
            "id",
            "username",
            "email",
            "user_type",
            "bio",
            "mobile",
            "address",
            "location",
            "pincode",
            "properties",
        )

        read_only_fields = (
            "username",
            "user_type",
        )


class AgentUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.CharField(source="user.email")
    properties = serializers.SlugRelatedField(
        many=True, queryset=PropertyModel.objects.all(), slug_field="text"
    )

    class Meta:
        model = AgentUserProfile
        fields = (
            "id",
            "username",
            "email",
            "user_type",
            "bio",
            "mobile",
            "address",
            "location",
            "pincode",
            "properties",
            "wishlist",
        )

        read_only_fields = (
            "username",
            "user_type",
        )
