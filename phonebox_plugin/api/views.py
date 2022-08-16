from rest_framework.routers import APIRootView
from .. import filters
from ..models import Number
from . import serializers
from django.conf import settings
from packaging import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)

if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
    from netbox.api.viewsets import NetBoxModelViewSet as ModelViewSet
else:
    from netbox.api.views import ModelViewSet


class PhoneBoxPluginRootView(APIRootView):
    """
    phonebox_plugin API root view
    """
    def get_view_name(self):
        return 'PhoneBox'


class NumberViewSet(ModelViewSet):
    queryset = Number.objects.prefetch_related('tenant', 'region', 'tags')
    serializer_class = serializers.NumberSerializer
    filterset_class = filters.NumberFilterSet