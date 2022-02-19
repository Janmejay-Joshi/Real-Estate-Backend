from random import randint
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from apps.messaging.models import OTPModel

from apps.profiles.models import PrimeModel, UserProfileModel


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        prime = PrimeModel.objects.create()
        user = UserProfileModel.objects.create(
            user=instance, prime_status=prime, mobile=f"{randint(0,10000000)}"
        )
        OTPModel.objects.create(user=user)
