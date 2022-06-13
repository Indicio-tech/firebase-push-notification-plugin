from marshmallow import EXCLUDE, fields

from ..message_types import MESSAGE_TYPES, GET_DEVICE_INFO

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema
from aries_cloudagent.core.profile import InjectionContext
from aries_cloudagent.core.protocol_registry import ProtocolRegistry
from aries_cloudagent.core.event_bus import EventBus

HANDLER_CLASS = "firebase_push_notification.v1_0.handlers.get_device_info_handler.GetDeviceInfoHandler"


class GetDeviceInfo(AgentMessage):
    """Class for getting device info."""

    class Meta:
        """Metadata for get device info."""
        handler_class = HANDLER_CLASS
        message_type = GET_DEVICE_INFO
        schema_class = "GetDeviceInfoSchema"

    def __init__(
        self,
        *,
        thread_id,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.thread_id = thread_id

async def setup(context: InjectionContext, protocol_registry: ProtocolRegistry = None):
    """Setup the connections plugin."""
    # if not protocol_registry:
    #     protocol_registry = context.inject(ProtocolRegistry)

    # protocol_registry.register_message_types(MESSAGE_TYPES)
    # event_bus = context.inject(EventBus)

    if not plugin_registry:
        plugin_registry = context.inject(PluginRegistry)
        # LOGGER.debug("This is the plugin registry: ", plugin_registry)

    plugin_registry.register_package("firebase_push_notification")


class GetDeviceInfoSchema(AgentMessageSchema):
    """Get device info schema class."""

    class Meta:
        """Get device info schema metadata."""

        model_class = GetDeviceInfo
        unknown = EXCLUDE

    thread_id = fields.Str(
        required=True,
        description="The token that is required by the notification provider",
    )
