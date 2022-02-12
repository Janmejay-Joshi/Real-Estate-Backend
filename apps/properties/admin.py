from django.contrib import admin

from apps.properties.models import AmenitiesTags, Image, PropertyModel

# Register your models here.

admin.site.register(PropertyModel)
admin.site.register(AmenitiesTags)

admin.site.register(Image)
