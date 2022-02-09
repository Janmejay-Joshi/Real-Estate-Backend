from django.db import models
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField, PPOIField

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


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = VersatileImageField("Image", upload_to="images/", ppoi_field="image_ppoi")
    image_ppoi = PPOIField()

    objects = models.Manager

    def __str__(self):
        return self.name


class PropertyModel(models.Model):
    """
    Data Model For Template Profile Inherited By The Main Profiles
    TODO: Implement Custom Validators
          https://docs.djangoproject.com/en/4.0/ref/validators/
    """

    # MultiValued Feilds

    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posted_by"
    )

    image = models.ManyToManyField("properties.Image", related_name="products", blank=True)

    amenities = models.ManyToManyField(
        AmenitiesTags, blank=True, related_name="amenities"
    )
    features = models.ManyToManyField(FeaturesTags, blank=True, related_name="features")

    # General Feilds

    name = models.SlugField(max_length=80)
    property_name = models.TextField(max_length=80)

    description = models.TextField(null=True, verbose_name="Property Description")
    address = models.CharField(max_length=255, verbose_name="Property Address")
    city = models.CharField(max_length=50, verbose_name="City")
    state = models.CharField(max_length=50, verbose_name="State")
    pincode = models.CharField(max_length=6)

    prime_property = models.BooleanField(default=False)
    price = models.BigIntegerField()
    property_size = models.IntegerField()

    availability = models.DateTimeField()

    FOR_TYPE_CHOICES = [
        ("sale", "Sale"),
        ("rent", "Rent"),
    ]

    BEDROOMS_TYPE_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5+", "5+"),
    ]

    BATHROOMS_TYPE_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4+", "4+"),
    ]

    FURNISHING_TYPE_CHOICES = [
        ("furnished", "Furnished"),
        ("semifurnished", "Semi furnished"),
        ("unfurnished", "Unfurnished"),
    ]

    PROPERTY_TYPE_CHOICES = [
        ("AP", "Apartment"),
        ("IH", "Independent House"),
        ("VI", "Villa"),
        ("BF", "Builder Floor"),
        ("PH", "Penthouse"),
        ("SA", "Studio Apartment"),
        ("OT", "Other"),
    ]

    POSSESSION_TYPE_CHOICES = [
        ("Under Construction", "Under Construction"),
        ("Ready To Move", "Ready To Move"),
    ]

    # Choice Based Feilds

    furnishing_status = models.CharField(max_length=25, choices=FURNISHING_TYPE_CHOICES)
    for_status = models.CharField(max_length=4, choices=FOR_TYPE_CHOICES)

    bathrooms = models.CharField(max_length=2, choices=BATHROOMS_TYPE_CHOICES)
    bedrooms = models.CharField(max_length=2, choices=BEDROOMS_TYPE_CHOICES)

    possession = models.CharField(max_length=25, choices=POSSESSION_TYPE_CHOICES)

    property_type = models.CharField(max_length=2, choices=PROPERTY_TYPE_CHOICES)

    # Auto Feilds
    timestamp = models.DateTimeField(auto_now_add=True)
    visits = models.IntegerField(default=0)

    objects = models.Manager()
