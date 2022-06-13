from marshmallow import fields, EXCLUDE

from ..message_types import SET_DEVICE_INFO, MESSAGE_TYPES

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema
from aries_cloudagent.core.profile import InjectionContext
from aries_cloudagent.core.protocol_registry import ProtocolRegistry
from aries_cloudagent.core.event_bus import EventBus

HANDLER_CLASS = "firebase_push_notification.v1_0.handlers.set_device_info_handler.SetDeviceInfoHandler"


class SetDeviceInfo(AgentMessage):
    """Class for setting device info."""

    class Meta:
        """Metadata for set device info."""

        handler_class = HANDLER_CLASS
        message_type = SET_DEVICE_INFO
        schema_class = "SetDeviceInfoSchema"

    def __init__(
        self,
        *,
        device_token: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.device_token = device_token

async def setup(context: InjectionContext, protocol_registry: ProtocolRegistry = None):
    """Setup the connections plugin."""
    if not protocol_registry:
        protocol_registry = context.inject(ProtocolRegistry)

    protocol_registry.register_message_types(MESSAGE_TYPES)
    event_bus = context.inject(EventBus)


class SetDeviceInfoSchema(AgentMessageSchema):
    """Set device info schema class."""

    class Meta:
        """Set device info schema metadata."""

        model_class = SetDeviceInfo
        unknown = EXCLUDE

    device_token = fields.Str(
        required=True,
        description="The token that is required by the notification provider",
    )
