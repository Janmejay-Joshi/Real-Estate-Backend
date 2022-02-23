from django.contrib import admin

from apps.properties.models import (
    AmenitiesTags,
    CityModel,
    Image,
    PropertyModel,
    SublocationModel,
)

# Register your models here.

admin.site.register(PropertyModel)
admin.site.register(AmenitiesTags)
admin.site.register(SublocationModel)
admin.site.register(CityModel)


admin.site.register(Image)
