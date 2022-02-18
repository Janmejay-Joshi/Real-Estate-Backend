from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus

# Create your models here.


class Order(models.Model):

    user = models.ForeignKey(
        "profiles.UserProfileModel",
        related_name="order_profile",
        on_delete=models.DO_NOTHING,
    )
    subscription_type = CharField(
        _("Subscription Type"),
        max_length=200,
        blank=False,
        null=False,
    )
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=200,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    objects = models.Manager()

    def __str__(self):
        return f"{self.id}-{self.user}-{self.status}"
