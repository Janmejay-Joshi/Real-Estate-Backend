from rest_framework import serializers

from apps.properties.models import AmenitiesTags, FeaturesTags, PropertyModel


class AmenitiesTagsSerializer(serializers.ModelSerializer):
    property = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = AmenitiesTags
        fields = "__all__"


class FeaturesTagsSerializer(serializers.ModelSerializer):
    property = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = FeaturesTags
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):

    features = serializers.SlugRelatedField(
        many=True, queryset=FeaturesTags.objects.all(), slug_field="text"
    )

    amenities = serializers.SlugRelatedField(
        many=True, queryset=AmenitiesTags.objects.all(), slug_field="text"
    )

    class Meta:
        model = PropertyModel
        fields = "__all__"
        read_only_fields = (
            "visits",
            "timestamp",
        )
