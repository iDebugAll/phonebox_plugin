from rest_framework.routers import APIRootView
from .. import filters
from ..models import Number
from netbox.api.views import ModelViewSet
from . import serializers


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
