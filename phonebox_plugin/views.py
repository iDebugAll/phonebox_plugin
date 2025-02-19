#!./venv/bin/python

from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from .models import Number, VoiceCircuit
from . import filters
from . import forms
from . import tables
from django.conf import settings
from packaging import version


@register_model_view(Number, "list", path="", detail=False)
class NumberListView(generic.ObjectListView):
    queryset = Number.objects.all()
    filterset = filters.NumberFilterSet
    filterset_form = forms.NumberFilterForm
    table = tables.NumberTable


@register_model_view(Number)
class NumberView(generic.ObjectView):
    queryset = Number.objects.prefetch_related('tenant')
    template_name = "phonebox_plugin/number.html"


@register_model_view(Number, "add", detail=False)
@register_model_view(Number, "edit")
class NumberEditView(generic.ObjectEditView):
    queryset = Number.objects.all()
    form = forms.NumberEditForm


@register_model_view(Number, "bulk_edit", path="edit", detail=False)
class NumberBulkEditView(generic.BulkEditView):
    queryset = Number.objects.prefetch_related('tenant')
    filterset = filters.NumberFilterSet
    table = tables.NumberTable
    form = forms.NumberBulkEditForm


@register_model_view(Number, "delete")
class NumberDeleteView(generic.ObjectDeleteView):
    queryset = Number.objects.all()


@register_model_view(Number, "bulk_delete", path="delete", detail=False)
class NumberBulkDeleteView(generic.BulkDeleteView):
    queryset = Number.objects.filter()
    filterset = filters.NumberFilterSet
    table = tables.NumberTable


@register_model_view(Number, "bulk_import", detail=False)
class NumberBulkImportView(generic.BulkImportView):
    queryset = Number.objects.all()
    model_form = forms.NumberCSVForm
    table = tables.NumberTable


@register_model_view(VoiceCircuit, "list", path="", detail=False)
class VoiceCircuitListView(generic.ObjectListView):
    queryset = VoiceCircuit.objects.all()
    filterset = filters.VoiceCircuitFilterSet
    filterset_form = forms.VoiceCircuitFilterForm
    table = tables.VoiceCircuitTable


@register_model_view(VoiceCircuit)
class VoiceCircuitView(generic.ObjectView):
    queryset = VoiceCircuit.objects.prefetch_related('tenant')
    template_name = "phonebox_plugin/voicecircuit.html"

@register_model_view(VoiceCircuit, "add", detail=False)
@register_model_view(VoiceCircuit, "edit")
class VoiceCircuitEditView(generic.ObjectEditView):
    queryset = VoiceCircuit.objects.all()
    form = forms.VoiceCircuitEditForm


@register_model_view(VoiceCircuit, "bulk_edit", path="edit", detail=False)
class VoiceCircuitBulkEditView(generic.BulkEditView):
    queryset = VoiceCircuit.objects.prefetch_related('tenant')
    filterset = filters.VoiceCircuitFilterSet
    table = tables.VoiceCircuitTable
    form = forms.VoiceCircuitBulkEditForm


@register_model_view(VoiceCircuit, "delete")
class VoiceCircuitDeleteView(generic.ObjectDeleteView):
    queryset = VoiceCircuit.objects.all()


@register_model_view(VoiceCircuit, "bulk_delete", path="delete", detail=False)
class VoiceCircuitBulkDeleteView(generic.BulkDeleteView):
    queryset = VoiceCircuit.objects.filter()
    filterset = filters.VoiceCircuitFilterSet
    table = tables.VoiceCircuitTable


@register_model_view(VoiceCircuit, "bulk_import", detail=False)
class VoiceCircuitBulkImportView(generic.BulkImportView):
    queryset = VoiceCircuit.objects.all()
    model_form = forms.VoiceCircuitCSVForm
    table = tables.VoiceCircuitTable
