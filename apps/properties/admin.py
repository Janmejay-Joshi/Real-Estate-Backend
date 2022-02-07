from django.contrib import admin

from apps.properties.models import AmenitiesTags, FeaturesTags, PropertyModel

# Register your models here.

admin.site.register(PropertyModel)
admin.site.register(FeaturesTags)
admin.site.register(AmenitiesTags)
