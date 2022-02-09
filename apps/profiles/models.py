from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL

from apps.properties.models import PropertyModel, Image


# Create your models here.


class UserProfileModel(models.Model):
    """
    Data Model For User Profile
    TODO: Implement Custom Validators
          https://docs.djangoproject.com/en/4.0/ref/validators/
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )

    image = models.OneToOneField(
        "properties.Image", null=True, related_name="cover", on_delete=SET_NULL
    )

    bio = models.TextField(blank=True, verbose_name="User Bio")
    mobile = models.CharField(max_length=10, verbose_name="Phone Number")
    address = models.CharField(max_length=255, verbose_name="User Address")
    city = models.CharField(max_length=50, verbose_name="City")
    state = models.CharField(max_length=50, verbose_name="State")
    pincode = models.CharField(max_length=6)
    is_prime = models.BooleanField(default=False)
    properties = models.ManyToManyField(
        PropertyModel, related_name="properties", blank=True
    )
    wishlist = models.ManyToManyField(
        PropertyModel, related_name="wishlist", blank=True
    )

    USER_TYPE_CHOICES = [
        ("Agent", "Agent"),
        ("Buyer", "Buyer"),
        ("Seller", "Seller"),
    ]

    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)
    objects = models.Manager()
