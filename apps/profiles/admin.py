from django.contrib import admin

from apps.profiles.models import AgentUserProfile, BuyerUserProfile, SellerUserProfile

# Register your models here.

admin.site.register(BuyerUserProfile)
admin.site.register(SellerUserProfile)
admin.site.register(AgentUserProfile)
