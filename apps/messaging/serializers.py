from rest_framework import serializers

from apps.messaging.models import OTPModel


class OTPSerializer(serializers.ModelSerializer):
    """
    Serve Data for AmenitiesTags Model
    """

    class Meta:
        model = OTPModel
        fields = "__all__"
