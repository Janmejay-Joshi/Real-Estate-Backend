from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

from apps.properties.models import AmenitiesTags, FeaturesTags, PropertyModel


class AmenitiesTagsSerializer(serializers.ModelSerializer):
    property = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = AmenitiesTags


class FeaturesTagsSerializer(serializers.ModelSerializer):
    property = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = FeaturesTags


class PropertySerializer(TaggitSerializer, serializers.ModelSerializer):

    features = serializers.SlugRelatedField(
        many=True, queryset=FeaturesTags.objects.all(), slug_field="text"
    )

    amenities = serializers.SlugRelatedField(
        many=True, queryset=AmenitiesTags.objects.all(), slug_field="text"
    )

    class Meta:
        model = PropertyModel
        fields = "__all__"
