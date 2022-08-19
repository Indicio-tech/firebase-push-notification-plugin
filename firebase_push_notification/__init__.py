__version__ = "1.0.0"
import logging
from aries_cloudagent.config.injection_context import InjectionContext
from aries_cloudagent.core.event_bus import EventBus
from aries_cloudagent.core.protocol_registry import ProtocolRegistry

from .v1_0.message_types import MESSAGE_TYPES

LOGGER = logging.getLogger(__name__)

from .v1_0.messages import (
    set_device_info,
    get_device_info,
    device_info,
    push_notification,
)

MODULES = [
    set_device_info,
    get_device_info,
    device_info,
    push_notification,
]


async def setup(context: InjectionContext, protocol_registry: ProtocolRegistry = None):
    """Setup the plugin."""
    bus = context.inject(EventBus)
    assert bus
    LOGGER.debug("Registering Firebase plugin")

    if not protocol_registry:
        protocol_registry = context.inject(ProtocolRegistry)
    protocol_registry.register_message_types(MESSAGE_TYPES)
