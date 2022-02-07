from django.db import models
from django.contrib.auth.models import User

from apps.properties.models import PropertyModel


# Create your models here.


class TemplateUserProfile(models.Model):
    """
    Data Model For Template Profile Inherited By The Main Profiles
    TODO: Implement Custom Validators
          https://docs.djangoproject.com/en/4.0/ref/validators/
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )

    bio = models.TextField(null=True, verbose_name="User Bio")
    mobile = models.CharField(max_length=10, verbose_name="Phone Number")
    address = models.CharField(max_length=255, verbose_name="User Address")
    location = models.CharField(max_length=50, verbose_name="Genral Location")
    pincode = models.CharField(max_length=6)
    is_prime = models.BooleanField(default=False)

    objects = models.Manager()


class SellerUserProfile(TemplateUserProfile):
    """
    Data Model For a Seller Type Account
    TODO: Implement Property
    """

    properties = models.ManyToManyField(
        PropertyModel, related_name="seller_properties", blank=True
    )
    user_type = models.CharField(max_length=6, default="Seller")
    objects = models.Manager()


class BuyerUserProfile(TemplateUserProfile):
    """
    Data Model For a Buyer Type Account
    TODO: Implement Property
    """

    wishlist = models.ManyToManyField(
        PropertyModel, related_name="buyer_wishlist", blank=True
    )
    user_type = models.CharField(max_length=6, default="Buyer")
    objects = models.Manager()


class AgentUserProfile(TemplateUserProfile):
    """
    Data Model For a Agent Type Account
    TODO: Implement Property
    """

    properties = models.ManyToManyField(
        PropertyModel, related_name="agent_properties", blank=True
    )
    wishlist = models.ManyToManyField(
        PropertyModel, related_name="agent_whitelist", blank=True
    )
    user_type = models.CharField(max_length=6, default="Agent")
    objects = models.Manager()
