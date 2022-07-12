#!./venv/bin/python

from netbox.views import generic
from .models      import Number, VoiceCircuit, PBX
from .            import filters
from .            import forms
from .            import tables

from django.conf  import settings
from packaging    import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)

# NUMBERS
class NumberListView(generic.ObjectListView):
    queryset = Number.objects.all()
    filterset = filters.NumberFilterSet
    filterset_form = forms.NumberFilterForm
    table = tables.NumberTable
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/number_list_3.x.html"
    else:
        template_name = "phonebox_plugin/number_list.html"


class NumberView(generic.ObjectView):
    queryset = Number.objects.prefetch_related('tenant')
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/number_3.x.html"
    else:
        template_name = "phonebox_plugin/number.html"


class NumberEditView(generic.ObjectEditView):
    queryset = Number.objects.all()

    if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
        form = forms.NumberEditForm
    else:
        model_form = forms.NumberEditForm

    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/number_add_3.x.html"
    else:
        template_name = "phonebox_plugin/number_add.html"


class NumberBulkEditView(generic.BulkEditView):
    queryset = Number.objects.prefetch_related('tenant')
    filterset = filters.NumberFilterSet
    table = tables.NumberTable
    form = forms.NumberBulkEditForm


class NumberDeleteView(generic.ObjectDeleteView):
    queryset = Number.objects.all()
    default_return_url = "plugins:phonebox_plugin:number_list"


class NumberBulkDeleteView(generic.BulkDeleteView):
    queryset = Number.objects.filter()
    filterset = filters.NumberFilterSet
    table = tables.NumberTable
    default_return_url = "plugins:phonebox_plugin:number_list"


class NumberBulkImportView(generic.BulkImportView):
    queryset = Number.objects.all()
    model_form = forms.NumberCSVForm
    table = tables.NumberTable

# VOICE CIRCUITS
class VoiceCircuitListView(generic.ObjectListView):
    queryset = VoiceCircuit.objects.all()
    filterset = filters.VoiceCircuitFilterSet
    filterset_form = forms.VoiceCircuitFilterForm
    table = tables.VoiceCircuitTable
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/voice_circuit_list_3.x.html"
    else:
        template_name = "phonebox_plugin/voice_circuit_list.html"


class VoiceCircuitView(generic.ObjectView):
    queryset = VoiceCircuit.objects.prefetch_related('tenant')
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/voice_circuit_3.x.html"
    else:
        template_name = "phonebox_plugin/voice_circuit.html"


class VoiceCircuitEditView(generic.ObjectEditView):
    queryset = VoiceCircuit.objects.all()

    if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
        form = forms.VoiceCircuitEditForm
    else:
        model_form = forms.VoiceCircuitEditForm

    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/voice_circuit_add_3.x.html"
    else:
        template_name = "phonebox_plugin/voice_circuit_add.html"


class VoiceCircuitBulkEditView(generic.BulkEditView):
    queryset = VoiceCircuit.objects.prefetch_related('tenant')
    filterset = filters.VoiceCircuitFilterSet
    table = tables.VoiceCircuitTable
    form = forms.VoiceCircuitBulkEditForm


class VoiceCircuitDeleteView(generic.ObjectDeleteView):
    queryset = VoiceCircuit.objects.all()
    default_return_url = "plugins:phonebox_plugin:voice_circuit_list"


class VoiceCircuitBulkDeleteView(generic.BulkDeleteView):
    queryset = VoiceCircuit.objects.filter()
    filterset = filters.VoiceCircuitFilterSet
    table = tables.VoiceCircuitTable
    default_return_url = "plugins:phonebox_plugin:voice_circuit_list"


class VoiceCircuitBulkImportView(generic.BulkImportView):
    queryset = VoiceCircuit.objects.all()
    model_form = forms.VoiceCircuitCSVForm
    table = tables.VoiceCircuitTable

# PBX'S
class PBXListView(generic.ObjectListView):
    queryset = PBX.objects.all()
    filterset = filters.PbxTelephonyFilterSet
    filterset_form = forms.PBXFilterForm
    table = tables.PBXTable
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/pbx_list_3.x.html"
    else:
        template_name = "phonebox_plugin/pbx_list.html"


class PBXView(generic.ObjectView):
    queryset = PBX.objects.prefetch_related('tenant')
    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/pbx_3.x.html"
    else:
        template_name = "phonebox_plugin/pbx.html"


class PBXEditView(generic.ObjectEditView):
    queryset = PBX.objects.all()

    if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
        form = forms.PBXEditForm
    else:
        model_form = forms.PBXEditForm

    if NETBOX_CURRENT_VERSION >= version.parse("3.0"):
        template_name = "phonebox_plugin/pbx_add_3.x.html"
    else:
        template_name = "phonebox_plugin/pbx_add.html"


class PBXBulkEditView(generic.BulkEditView):
    queryset = PBX.objects.prefetch_related('tenant')
    filterset = filters.PbxTelephonyFilterSet
    table = tables.PBXTable
    form = forms.PBXBulkEditForm


class PBXDeleteView(generic.ObjectDeleteView):
    queryset = PBX.objects.all()
    default_return_url = "plugins:phonebox_plugin:pbx_list"


class PBXBulkDeleteView(generic.BulkDeleteView):
    queryset = PBX.objects.filter()
    filterset = filters.PbxTelephonyFilterSet
    table = tables.PBXTable
    default_return_url = "plugins:phonebox_plugin:pbx_list"


class PBXBulkImportView(generic.BulkImportView):
    queryset = PBX.objects.all()
    model_form = forms.PBXCSVForm
    table = tables.PBXTable