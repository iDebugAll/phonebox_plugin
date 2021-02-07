import django_filters
from utilities.filters import BaseFilterSet, TagFilter
from django.db.models import Q
from dcim.models import Region
from tenancy.models import Tenant
from .models import Number


class NumberFilterSet(BaseFilterSet):

    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    number = django_filters.ModelMultipleChoiceFilter(
        field_name='number',
        queryset=Number.objects.all(),
        to_field_name='number',
        label='number',
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label='Tenant (ID)',
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        field_name='tenant__slug',
        to_field_name='slug',
        label='Tenant (slug)',
    )
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='region__slug',
        to_field_name='slug',
        label='Region (slug)',
    )
    forward_to = django_filters.ModelMultipleChoiceFilter(
        field_name='forward_to',
        queryset=Number.objects.all(),
        to_field_name='number',
        label='forward_to',
    )
    tag = TagFilter()

    class Meta():
        model = Number
        fields = ('number',)

    def search(self, queryset, number, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(number__icontains=value)
        )
