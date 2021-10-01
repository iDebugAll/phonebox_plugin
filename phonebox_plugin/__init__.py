from extras.plugins import PluginConfig


class PhoneBoxConfig(PluginConfig):
    name = 'phonebox_plugin'
    verbose_name = 'PhoneBox Plugin'
    description = 'Telephone Number Management Plugin for NetBox.'
    version = 'v0.0.2-beta.1'
    author = 'Igor Korotchenkov'
    author_email = 'iDebugAll@gmail.com'
    base_url = 'phonebox'
    min_version = "2.11.0"
    required_settings = []
    default_settings = {}
    caching_config = {
        '*': None
    }

config = PhoneBoxConfig
