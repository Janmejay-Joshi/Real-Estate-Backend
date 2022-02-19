from django.db import models

# Create your models here.


class OTPModel(models.Model):

    user = models.ForeignKey(
        "profiles.UserProfileModel", on_delete=models.CASCADE, related_name="otp_user"
    )

    otp = models.SmallIntegerField(null=True)

    objects = models.Manager()
