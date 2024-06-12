from packaging import version
from django.conf import settings
NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)

if NETBOX_CURRENT_VERSION >= version.parse("4.0.0"):
    from netbox.plugins import PluginMenuItem
else:
    from extras.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link='plugins:phonebox_plugin:list_view',
        link_text='Numbers',
        buttons=()
    ),
    PluginMenuItem(
        link='plugins:phonebox_plugin:voice_circuit_list_view',
        link_text='Voice Circuits',
        buttons=()
    ),
)
