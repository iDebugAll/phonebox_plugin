from packaging import version
from django.conf import settings
NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)

if NETBOX_CURRENT_VERSION >= version.parse("4.0.0"):
    from netbox.plugins import PluginConfig
else:
    from extras.plugins import PluginConfig


class PhoneBoxConfig(PluginConfig):
    name = 'phonebox_plugin'
    verbose_name = 'PhoneBox Plugin'
    description = 'Telephone Number Management Plugin for NetBox.'
    version = 'v0.0.10'
    author = 'Igor Korotchenkov'
    author_email = 'iDebugAll@gmail.com'
    base_url = 'phonebox'
    min_version = "4.1.0"
    required_settings = []
    default_settings = {}
    caching_config = {
        '*': None
    }

config = PhoneBoxConfig
