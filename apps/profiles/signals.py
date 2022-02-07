from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from apps.profiles.models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(created, instance, kwargs)
        # UserProfile.objects.create(user=instance)
