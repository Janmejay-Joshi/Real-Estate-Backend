from rest_framework import serializers

from apps.properties.models import AmenitiesTags, FeaturesTags, PropertyModel, Image
from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_flex_fields import FlexFieldsModelSerializer


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


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("full_size", "url"),
            ("thumbnail", "thumbnail__100x100"),
        ]
    )

    class Meta:
        model = Image
        fields = ["pk", "name", "image"]


class PropertySerializer(FlexFieldsModelSerializer):

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
        expandable_fields = {
            "image": ("reviews.ImageSerializer", {"many": True}),
        }
