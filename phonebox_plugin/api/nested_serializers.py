from rest_framework import serializers
from phonebox_plugin import models
from netbox.api import WritableNestedSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer

__all__ = ["NestedNumberSerializer", ]


class NestedNumberSerializer(WritableNestedSerializer):

    tenant = NestedTenantSerializer(required=True, allow_null=False)

    class Meta:
        model = models.Number
        fields = [
            "id", "number", "tenant",
        ]
