from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from ..models import Number
from tenancy.api.nested_serializers import NestedTenantSerializer
from dcim.api.nested_serializers import NestedRegionSerializer
from circuits.api.nested_serializers import NestedProviderSerializer
from extras.api.serializers import TagSerializer
from .nested_serializers import NestedNumberSerializer
from extras.api.nested_serializers import NestedTagSerializer


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
