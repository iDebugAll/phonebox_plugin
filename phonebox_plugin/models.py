from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from extras.models import TaggedItem
from netbox.models import ChangeLoggedModel
from utilities.querysets import RestrictedQuerySet
from django.core.validators import RegexValidator
from taggit.managers import TaggableManager
from django.urls import reverse
from .choices import VoiceCircuitTypeChoices, VOICE_CIRCUIT_ASSIGNMENT_MODELS

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


class VoiceCircuit(ChangeLoggedModel):
    """A Voice Circuit represents a single circuit of one of the following types:
    - SIP Trunk.
    - Digital Voice Circuit (BRI/PRI/etc).
    - Analog Voice Circuit (CO lines).
    """

    name = models.CharField(max_length=64)
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    description = models.CharField(max_length=200, blank=True)
    voice_circuit_type = models.CharField(
        max_length=50,
        choices=VoiceCircuitTypeChoices,
        blank=False
    )
    provider = models.ForeignKey(
        to="circuits.Provider",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="vc_provider_set"
    )
    provider_circuit_id = models.CharField(
        max_length=50,
        blank=True
    )
    region = models.ForeignKey(
        to="dcim.Region",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="vc_region_set"
    )
    site = models.ForeignKey(
        to="dcim.Site",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="vc_site_set"
    )
    tags = TaggableManager(through=TaggedItem)

    sip_source = models.CharField(
        max_length=255,
        blank=True
    )
    sip_target = models.CharField(
        max_length=255,
        blank=True
    )

    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=VOICE_CIRCUIT_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )

    objects = RestrictedQuerySet.as_manager()

    csv_headers = ['name', 'voice_circuit_type', 'tenant', 'region', 'site', 'description', 'provider']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("plugins:phonebox_plugin:voice_circuit_view", kwargs={"pk": self.pk})
