from django import forms
from django.conf import settings
from packaging import version
from tenancy.models import Tenant
from dcim.models import Region, Site, Device, Interface
from virtualization.models import VirtualMachine, VMInterface
from circuits.models import Provider
from extras.models import Tag
from .models import Number, VoiceCircuit
from .choices import VoiceCircuitTypeChoices

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION < version.parse("3.5"):
    from utilities.forms import (
        BootstrapMixin, DynamicModelMultipleChoiceField, DynamicModelChoiceField,
        TagFilterField, BulkEditForm, CSVModelForm, CSVModelChoiceField
    )
else:
    from utilities.forms import BootstrapMixin, BulkEditForm, CSVModelForm
    from utilities.forms.fields import (
        DynamicModelMultipleChoiceField, DynamicModelChoiceField,
        TagFilterField, CSVModelChoiceField
    )

class AddRemoveTagsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add add/remove tags fields
        self.fields['add_tags'] = DynamicModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            required=False
        )
        self.fields['remove_tags'] = DynamicModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            required=False
        )


class NumberFilterForm(forms.Form):

    model = Number
    q = forms.CharField(
        required=False,
        label='Search'
    )
    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    provider = DynamicModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    tags = TagFilterField(model)


class NumberEditForm(forms.ModelForm):

    number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'pattern': r'^\+?[0-9A-D\*\#]+$',
                'title': 'Enter the Phone Number'
            }
        )
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    
    class Meta:
        model = Number
        fields = ('number', 'tenant', 'region', 'description', 'provider', 'forward_to', 'tags')


class NumberBulkEditForm(AddRemoveTagsForm, BulkEditForm):

    pk = forms.ModelMultipleChoiceField(
        queryset=Number.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    # Implement plugin API to migrate to DynamicModelChoiceField
    forward_to = forms.ModelChoiceField(
        queryset=Number.objects.all(),
        to_field_name="number",
        required=False
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )

    class Meta:
        nullable_fields = ('region', 'provider', 'forward_to', 'description')


class NumberCSVForm(CSVModelForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text='Assigned tenant'
    )
    provider = CSVModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Originating provider'
    )
    region = CSVModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Assigned region'
    )
    forward_to = CSVModelChoiceField(
        queryset=Number.objects.all(),
        to_field_name="number",
        required=False
    )

    class Meta:
        model = Number
        fields = Number.csv_headers
        help_texts = {
            'forward_to': "Optional call forwarding Number",
        }


class VoiceCircuitEditForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
    )
    voice_circuit_type = forms.ChoiceField(
        choices=VoiceCircuitTypeChoices,
        widget=forms.Select(attrs={"onChange": 'ShowVCTypeRelatedDetails();'})
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        initial_params={
            'interfaces': '$interface'
        }
    )
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        query_params={
            'device_id': '$device'
        }
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        initial_params={
            'interfaces': '$vminterface'
        }
    )
    vminterface = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        required=False,
        label='Interface',
        query_params={
            'virtual_machine_id': '$virtual_machine'
        }
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    class Media:
        js = ('phonebox_plugin/js/edit_virtual_circuit.js',)

    class Meta:
        model = VoiceCircuit
        fields = (
            'name', 'voice_circuit_type', 'tenant', 'region', 'site',
            'description', 'provider', 'provider_circuit_id', 'tags',
            'sip_source', 'sip_target'
        )

    def __init__(self, *args, **kwargs):

        # Initialize helper selectors
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {}).copy()
        if instance:
            if type(instance.assigned_object) is Interface:
                initial['interface'] = instance.assigned_object
            elif type(instance.assigned_object) is VMInterface:
                initial['vminterface'] = instance.assigned_object

        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        # Cannot select both a device interface and a VM interface
        if self.cleaned_data.get('interface') and self.cleaned_data.get('vminterface'):
            raise forms.ValidationError("Cannot select both a device interface and a virtual machine interface")
        if not (self.cleaned_data.get('interface') or self.cleaned_data.get('vminterface')):
            raise forms.ValidationError("Voice Circuit must be attached to a device interface or a VM interface")
        self.instance.assigned_object = self.cleaned_data.get('interface') or self.cleaned_data.get('vminterface')


class VoiceCircuitFilterForm(forms.Form):

    model = VoiceCircuit
    q = forms.CharField(
        required=False,
        label='Search'
    )
    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    provider = DynamicModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    tags = TagFilterField(model)


class VoiceCircuitBulkEditForm(AddRemoveTagsForm, BulkEditForm):

    pk = forms.ModelMultipleChoiceField(
        queryset=VoiceCircuit.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='id',
        required=False,
        null_option='None',
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )

    class Meta:
        nullable_fields = ('region', 'provider', 'description')


class VoiceCircuitCSVForm(CSVModelForm):

    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text='Assigned tenant'
    )
    provider = CSVModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Originating provider'
    )
    site = CSVModelChoiceField(
        queryset=Site.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Assigned site'
    )
    region = CSVModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Assigned region'
    )
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Parent device of assigned interface (if any)'
    )
    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Parent VM of assigned interface (if any)'
    )
    interface = CSVModelChoiceField(
        queryset=Interface.objects.none(),  # Can also refer to VMInterface
        required=True,
        to_field_name='name',
        help_text='Assigned interface'
    )

    class Meta:
        model = VoiceCircuit
        fields = [
            'name', 'voice_circuit_type', 'tenant', 'region', 'site',
            'description', 'provider', 'provider_circuit_id', 'device',
            'virtual_machine', 'interface',
        ]
