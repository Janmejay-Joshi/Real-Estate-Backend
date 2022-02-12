from django.contrib import admin

from apps.profiles.models import UserProfileModel, Contacted

# Register your models here.

admin.site.register(UserProfileModel)
admin.site.register(Contacted)
