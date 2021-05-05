from django.db import models
from extras.models import TaggedItem
from netbox.models import ChangeLoggedModel
from utilities.querysets import RestrictedQuerySet
from django.core.validators import RegexValidator
from taggit.managers import TaggableManager
from django.urls import reverse

number_validator = RegexValidator(
    r"^\+?[0-9A-D\#\*]*$",
    "Numbers can only contain: leading +, digits 0-9; chars A, B, C, D; # and *"
)


class Number(ChangeLoggedModel):
    """A Number represents a single telephone number of an arbitrary format.
    A Number can contain only valid DTMF characters and leading plus sign for E.164 support:
      - leading plus ("+") sign (optional)
      - digits 0-9
      - characters A, B, C, D
      - pound sign ("#")
      - asterisk sign ("*")
    Digit delimiters are now allowed. They will be implemented as a separate output formatter function.
    Number values can be not unique.
    Tenant is a mandatory option representing a number partition. Number and Tenant are globally unique.
    A Number can optionally be assigned with Provider and Region relations.
    A Number can contain an optional Description.
    A Number can optionally be tagged with Tags.
    """

    number = models.CharField(max_length=32, validators=[number_validator])
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    description = models.CharField(max_length=200, blank=True)
    provider = models.ForeignKey(
        to="circuits.Provider",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="provider_set"
    )
    region = models.ForeignKey(
        to="dcim.Region",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="region_set"
    )
    forward_to = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="forward_to_set"
    )
    tags = TaggableManager(through=TaggedItem)

    objects = RestrictedQuerySet.as_manager()

    csv_headers = ['number', 'tenant', 'region', 'description', 'provider', 'forward_to']

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse("plugins:phonebox_plugin:number_view", kwargs={"pk": self.pk})

    class Meta:
        unique_together = ("number", "tenant",)
