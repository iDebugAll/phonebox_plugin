from django import forms
from utilities.forms import (
    BootstrapMixin, DynamicModelMultipleChoiceField, DynamicModelChoiceField,
    TagFilterField, BulkEditForm, CSVModelForm, CSVModelChoiceField
)
from extras.forms import AddRemoveTagsForm
from tenancy.models import Tenant
from dcim.models import Region, Site
from circuits.models import Provider
from extras.models import Tag
from .models import Number, VoiceCircuit


class NumberFilterForm(BootstrapMixin, forms.Form):

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
    tag = TagFilterField(model)


class NumberEditForm(BootstrapMixin, forms.ModelForm):

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


class NumberBulkEditForm(BootstrapMixin, AddRemoveTagsForm, BulkEditForm):

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


class VoiceCircuitEditForm(BootstrapMixin, forms.ModelForm):

    name = forms.CharField(
        required=True,
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = VoiceCircuit
        fields = ('name', 'voice_circuit_type', 'tenant', 'region', 'site', 'description', 'provider', 'tags')


class VoiceCircuitFilterForm(BootstrapMixin, forms.Form):

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
    tag = TagFilterField(model)


class VoiceCircuitBulkEditForm(BootstrapMixin, AddRemoveTagsForm, BulkEditForm):

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

    class Meta:
        model = VoiceCircuit
        fields = VoiceCircuit.csv_headers
