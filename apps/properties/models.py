from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import Choices
from taggit.managers import TaggableManager

# Create your models here.


class AmenitiesTags(models.Model):
    text = models.CharField(max_length=64, unique=True)

    objects = models.Manager

    def __str__(self):
        return "Tag[id: {id}, text: {text}]".format(id=self.id, text=self.text)


class FeaturesTags(models.Model):
    text = models.CharField(max_length=64, unique=True)

    objects = models.Manager

    def __str__(self):
        return "Tag[id: {id}, text: {text}]".format(id=self.id, text=self.text)


class PropertyModel(models.Model):
    """
    Data Model For Template Profile Inherited By The Main Profiles
    TODO: Implement Custom Validators
          https://docs.djangoproject.com/en/4.0/ref/validators/
    """

    posted_by = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="posted_by"
    )
    name = models.SlugField(max_length=80)

    description = models.TextField(null=True, verbose_name="User Bio")
    address = models.CharField(max_length=255, verbose_name="User Address")
    location = models.CharField(max_length=50, verbose_name="Genral Location")
    pincode = models.CharField(max_length=6)

    prime_property = models.BooleanField(default=False)
    price = models.BigIntegerField()
    property_size = models.SmallIntegerField()
    furnishing_status = models.BooleanField()

    timestamp = models.DateTimeField()

    availability = models.CharField(max_length=100)
    bedrooms = models.SmallIntegerField()
    bathrooms = models.SmallIntegerField()

    amenities = models.ManyToManyField(AmenitiesTags, related_name="libraries")
    features = models.ManyToManyField(FeaturesTags, related_name="libraries")
    visits = models.IntegerField(default=0)

    PROPERTY_TYPE_CHOICES = [
        ("A", "Apartment"),
        ("I", "Independent House"),
        ("V", "Villa"),
        ("B", "Builder Floor"),
        ("P", "Penthouse"),
        ("S", "Studio Apartment"),
        ("O", "Other"),
    ]

    property_type = models.CharField(max_length=2, choices=PROPERTY_TYPE_CHOICES)

    # - images: ( 1-M ) { Images } Max(8)

    objects = models.Manager()
    url = models.URLField()
