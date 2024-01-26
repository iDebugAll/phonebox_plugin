from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from ..models import Number, VoiceCircuit
from tenancy.api.nested_serializers import NestedTenantSerializer
from dcim.api.nested_serializers import NestedRegionSerializer, NestedSiteSerializer
from circuits.api.nested_serializers import NestedProviderSerializer
from extras.api.serializers import TagSerializer
from .nested_serializers import NestedNumberSerializer
from extras.api.nested_serializers import NestedTagSerializer
from netbox.api.fields import ContentTypeField
from netbox.constants import NESTED_SERIALIZER_PREFIX
from utilities.api import get_serializer_for_model
from ..choices import VOICE_CIRCUIT_ASSIGNMENT_MODELS


class NumberSerializer(TagSerializer, serializers.ModelSerializer):

    label = serializers.CharField(source='number', read_only=True)
    tenant = NestedTenantSerializer(required=True, allow_null=False)
    region = NestedRegionSerializer(required=False, allow_null=True)
    provider = NestedProviderSerializer(required=False, allow_null=True)
    forward_to = NestedNumberSerializer(required=False, allow_null=True)
    tags = NestedTagSerializer(many=True, required=False)

    class Meta:
        model = Number
        fields = [
            "id", "label", "number", "tenant", "region", "forward_to", "description", "provider", "tags",
        ]


class VoiceCircuitSerializer(TagSerializer, serializers.ModelSerializer):

    label = serializers.CharField(source='voice_circuit', read_only=True)
    tenant = NestedTenantSerializer(required=True, allow_null=False)
    region = NestedRegionSerializer(required=False, allow_null=True)
    site = NestedSiteSerializer(required=False, allow_null=True)
    provider = NestedProviderSerializer(required=False, allow_null=True)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(VOICE_CIRCUIT_ASSIGNMENT_MODELS),
        required=True,
        allow_null=False
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)
    tags = NestedTagSerializer(many=True, required=False)

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object, prefix=NESTED_SERIALIZER_PREFIX)
        context = {'request': self.context['request']}
        return serializer(obj.assigned_object, context=context).data

    class Meta:
        model = VoiceCircuit
        fields = [
            "id", "label", "name", "voice_circuit_type", "tenant", "region", "site", "description",
            'assigned_object_type','assigned_object_id', 'assigned_object',
            "sip_source", "sip_target", "provider", "tags",
        ]
