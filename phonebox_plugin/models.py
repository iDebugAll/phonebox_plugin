from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from extras.models import TaggedItem
from netbox.models import ChangeLoggedModel
from utilities.querysets import RestrictedQuerySet
from django.core.validators import RegexValidator
from taggit.managers import TaggableManager
from django.urls import reverse
from .choices import VoiceCircuitTypeChoices, VOICE_CIRCUIT_ASSIGNMENT_MODELS, PBXTypeChoices, PBX_ASSIGNMENT_MODELS, NUMBER_ASSIGNMENT_MODELS

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
    fio = models.CharField(max_length=200, blank=True)
    pbx = models.ForeignKey(
        to='phonebox_plugin.PBX',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name = "num_pbx_set"
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_query_name='tennantgroup'
    )
    tenantgroup = models.ForeignKey(
        to='tenancy.TenantGroup',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    region = models.ForeignKey(
        to="dcim.Region",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="num_region_set"
    )
    site = models.ForeignKey(
        to="dcim.Site",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="num_site_set"
    )
    tags = TaggableManager(through=TaggedItem)
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name = "num_device_set"
    )
    is_record = models.BooleanField()
    access_cat = models.CharField(
        max_length=32,
        blank=True,
        null=True,
    )
    forward_to = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="num_forward_to_set"
    )
    provider = models.ForeignKey(
        to="circuits.Provider",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="num_provider_set"
    )
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=NUMBER_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='number_assign',
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
    comment = models.CharField(max_length=200, blank=True)

    objects = RestrictedQuerySet.as_manager()

    csv_headers = ['number', 'pbx', 'tenant', 'provider', 'region', 'site', 'device', 'is_record', 'access_cat', 'forward_to']

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse("plugins:phonebox_plugin:number_view", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['tenantgroup', 'tenant']

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
    pbx = models.ForeignKey(
        to='phonebox_plugin.PBX',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name = "vc_pbx_set"
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
        max_length=200,
        blank=True
    )
    sip_target = models.CharField(
        max_length=200,
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

class PBX(ChangeLoggedModel):

    name = models.CharField(
        max_length=64
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    pbx_type = models.CharField(
        max_length=50,
        choices=PBXTypeChoices,
        blank=False
    )
    is_virtual = models.BooleanField(
    )
    region = models.ForeignKey(
        to="dcim.Region",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="pbx_region_set"
    )
    site = models.ForeignKey(
        to="dcim.Site",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="pbx_site_set"
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    tags = TaggableManager(through=TaggedItem)
    domain = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    protocol = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    port = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    sip_proxy1 = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    sip_proxy2 = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=PBX_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='pbx_assign',
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

    csv_headers = ['name', 'pbx_type', 'region', 'site']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("plugins:phonebox_plugin:pbx_view", kwargs={"pk": self.pk})

