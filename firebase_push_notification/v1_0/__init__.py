__version__ = "1.0.0"
import logging

from aries_cloudagent.config.injection_context import InjectionContext
from aries_cloudagent.core.event_bus import EventBus
from aries_cloudagent.core.plugin_registry import PluginRegistry

LOGGER = logging.getLogger(__name__)


# async def setup(context: InjectionContext, plugin_registry: PluginRegistry = None):
#     """Setup the plugin."""
#     bus = context.inject(EventBus)
#     assert bus
#     LOGGER.debug("Registering Firebase plugin")

#     if not plugin_registry:
#         plugin_registry = context.inject(PluginRegistry)

#     plugin_registry.register_package("firebase_push_notification.v1_0")