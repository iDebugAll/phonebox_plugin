import django_tables2 as tables
from   .models        import Number, VoiceCircuit, PBX
from   django.conf    import settings
from   packaging      import version

NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)

if NETBOX_CURRENT_VERSION >= version.parse("3.2"):
    from netbox.tables import BaseTable, columns
    ToggleColumn = columns.ToggleColumn
else:
    from utilities.tables import BaseTable, ToggleColumn


class NumberTable(BaseTable):

    pk         = ToggleColumn()
    number     = tables.LinkColumn()
    fio        = tables.LinkColumn()
    pbx        = tables.LinkColumn()
    tenant     = tables.LinkColumn()
    tenantgroup= tables.LinkColumn()
    region     = tables.LinkColumn()
    site       = tables.LinkColumn()
    provider   = tables.LinkColumn()
    device     = tables.LinkColumn()
    is_record  = tables.LinkColumn()
    access_cat = tables.LinkColumn()
    forward_to = tables.LinkColumn()
    comment    = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model  = Number
        fields = ('pk', 'number', 'fio', 'pbx', 'tenant', 'tenantgroup', 'region', 'site', 'provider', 'device', 'is_record', 'access_cat', 'forward_to')
#        fields = ('pk', 'number', 'fio', 'tenant', 'region', 'site', 'provider', 'device', 'is_record', 'access_cat', 'forward_to', 'comment')


class VoiceCircuitTable(BaseTable):

    pk                 = ToggleColumn()
    name               = tables.LinkColumn()
    voice_device_or_vm = tables.Column(
        accessor='assigned_object.parent_object',
        linkify=True,
        orderable=False,
        verbose_name='Device/VM'
    )
    pbx                = tables.LinkColumn()
    voice_circuit_type = tables.LinkColumn()
    tenant             = tables.LinkColumn()
    region             = tables.LinkColumn()
    site               = tables.LinkColumn()
    provider           = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model  = VoiceCircuit
#        fields = ('pk', 'name', 'pbx', 'voice_device_or_vm', 'voice_circuit_type', 'tenant', 'region', 'site', 'provider')
        fields = ('pk', 'name', 'voice_device_or_vm', 'voice_circuit_type', 'tenant', 'region', 'site', 'provider')

class PBXTable(BaseTable):

    pk                 = ToggleColumn()
    name               = tables.LinkColumn()
    description        = tables.LinkColumn()
    voice_device_or_vm = tables.Column(
        accessor='assigned_object.parent_object',
        linkify=True,
        orderable=False,
        verbose_name='Device/VM'
    )
    region             = tables.LinkColumn()
    site               = tables.LinkColumn()
    pbx_type           = tables.LinkColumn()
    is_virtual         = tables.LinkColumn()
    domain             = tables.LinkColumn()
    protocol           = tables.LinkColumn()
    port               = tables.LinkColumn()
    sip_proxy1         = tables.LinkColumn()
    sip_proxy2         = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model  = PBX
        fields = ('pk', 'name', 'voice_device_or_vm', 'region', 'site', 'pbx_type', 'is_virtual')
#        fields = ('pk', 'name', 'region', 'site', 'pbx_type')