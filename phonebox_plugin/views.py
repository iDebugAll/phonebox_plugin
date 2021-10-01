#!./venv/bin/python

from netbox.views import generic
from .models import Number
from . import filters
from . import forms
from . import tables

from django.conf import settings
from packaging import version


NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)


class NumberListView(generic.ObjectListView):
    queryset = Number.objects.all()
    filterset = filters.NumberFilterSet
    filterset_form = forms.NumberFilterForm
    table = tables.NumberTable
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/list_view_3.x.html"
    else:
        template_name = "phonebox_plugin/list_view.html"


class NumberView(generic.ObjectView):
    queryset = Number.objects.prefetch_related('tenant')
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/number_3.x.html"
    else:
        template_name = "phonebox_plugin/number.html"


class NumberEditView(generic.ObjectEditView):
    queryset = Number.objects.all()
    model_form = forms.NumberEditForm
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/add_number_3.x.html"
    else:
        template_name = "phonebox_plugin/add_number.html"


class NumberBulkEditView(generic.BulkEditView):
    queryset = Number.objects.prefetch_related('tenant')
    filterset = filters.NumberFilterSet
    table = tables.NumberTable
    form = forms.NumberBulkEditForm


class NumberDeleteView(generic.ObjectDeleteView):
    queryset = Number.objects.all()
    default_return_url = "plugins:phonebox_plugin:list_view"


class NumberBulkDeleteView(generic.BulkDeleteView):
    queryset = Number.objects.filter()
    filterset = filters.NumberFilterSet
    table = tables.NumberTable
    default_return_url = "plugins:phonebox_plugin:list_view"


class NumberBulkImportView(generic.BulkImportView):
    queryset = Number.objects.all()
    model_form = forms.NumberCSVForm
    table = tables.NumberTable
