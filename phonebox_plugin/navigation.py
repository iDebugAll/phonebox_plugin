from packaging import version
from django.conf import settings

from netbox.plugins import PluginMenuItem, PluginMenu, PluginMenuButton

plugin_settings = settings.PLUGINS_CONFIG["phonebox_plugin"]


plugin_menu = (
    PluginMenuItem(
        link='plugins:phonebox_plugin:number_list',
        link_text='Numbers',
        permissions=["phonebox_plugin.view_number"],
        buttons=(
            PluginMenuButton(
                link="plugins:phonebox_plugin:number_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["phonebox_plugin.add_number"],
            ),
            PluginMenuButton(
                link="plugins:phonebox_plugin:number_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
                permissions=["phonebox_plugin.add_number"],
            ),
        ),
    ),
    PluginMenuItem(
        link='plugins:phonebox_plugin:voicecircuit_list',
        link_text='Voice Circuits',
        permissions=["phonebox_plugin.view_voicecircuit"],
        buttons=(
            PluginMenuButton(
                link="plugins:phonebox_plugin:voicecircuit_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                permissions=["phonebox_plugin.add_voicecircuit"],
            ),
            PluginMenuButton(
                link="plugins:phonebox_plugin:voicecircuit_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
                permissions=["phonebox_plugin.add_voicecircuit"],
            ),
        ),
    ),
)

if plugin_settings.get("top_level_menu"):
    menu = PluginMenu(
        label="PhoneBox Plugin",
        groups=(("Voice", plugin_menu),),
        icon_class="mdi mdi-phone-dial",
    )
else:
    menu_items = plugin_menu
