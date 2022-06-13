__version__ = "1.0.0"
import re
import logging
from aries_cloudagent.config.injection_context import InjectionContext
from aries_cloudagent.core.event_bus import Event, EventBus
from aries_cloudagent.core.profile import Profile
# from aries_cloudagent.core.protocol_registry import ProtocolRegistry

# from .v1_0.message_types import MESSAGE_TYPES

LOGGER = logging.getLogger(__name__)

# from .v1_0.messages import (
#     set_device_info,
#     get_device_info,
#     device_info,
#     push_notification,
# )

# MODULES = [
#     set_device_info,
#     get_device_info,
#     device_info,
#     push_notification,
# ]

from aries_cloudagent.core.plugin_registry import PluginRegistry

async def setup(context: InjectionContext, plugin_registry: PluginRegistry = None):
    """Setup the plugin."""
    bus = context.inject(EventBus)
    assert bus
    LOGGER.debug("Registering Firebase plugin")

    # for mod in MODULES:
    #     await mod.setup(context)

    # LOGGER.debug("Here are the message types: ", type(MESSAGE_TYPES), MESSAGE_TYPES)

    # if not plugin_registry:
    #     plugin_registry = context.inject(PluginRegistry)
    #     # LOGGER.debug("This is the plugin registry: ", plugin_registry)

    # plugin_registry.register_package("firebase_push_notification.v1_0")
