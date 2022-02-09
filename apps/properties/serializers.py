from rest_framework import serializers

from apps.properties.models import AmenitiesTags, FeaturesTags, PropertyModel, Image
from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_flex_fields import FlexFieldsModelSerializer


class AmenitiesTagsSerializer(serializers.ModelSerializer):
    """
    Serve Data for AmenitiesTags Model
    """

    property = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = AmenitiesTags
        fields = "__all__"


class FeaturesTagsSerializer(serializers.ModelSerializer):
    """
    Serve Data for FeaturesTags Model
    """

    property = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = FeaturesTags
        fields = "__all__"


class ImageSerializer(FlexFieldsModelSerializer):
    """
    Serve Data for Image Model and Resizes Uploaded Images for Thumbnail and Full Resolution
    """

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
    """
    Serve Data for Property Model has an Expandable Fields for Images
    """

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
