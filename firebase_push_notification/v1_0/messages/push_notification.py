from marshmallow import fields, EXCLUDE

from ..message_types import MESSAGE_TYPES, PUSH_NOTIFICATION

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema
from aries_cloudagent.core.profile import InjectionContext
from aries_cloudagent.core.protocol_registry import ProtocolRegistry
from aries_cloudagent.core.event_bus import EventBus


HANDLER_CLASS = "firebase_push_notification.v1_0.handlers.push_notification_handler.PushNotificationHandler"


class PushNotification(AgentMessage):

    class Meta:
        """Metadata for push notifications"""

        handler_class = HANDLER_CLASS
        message_type = PUSH_NOTIFICATION
        schema_class = "PushNotificationSchema"

    def __init__(
        self,
        *,
        message_tag: str = None,
        recipient_key: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.message_tag = message_tag
        self.recipient_key = recipient_key

async def setup(context: InjectionContext, protocol_registry: ProtocolRegistry = None):
    """Setup the connections plugin."""
    if not protocol_registry:
        protocol_registry = context.inject(ProtocolRegistry)

    protocol_registry.register_message_types(MESSAGE_TYPES)
    event_bus = context.inject(EventBus)


class PushNotificationSchema(AgentMessageSchema):
    """Push notification schema class."""

    class Meta:
        """Push notification schema metadata."""

        model_class = PushNotification
        unknown = EXCLUDE

    message_tag = fields.Str(
        required=False,
        description="Optional field to connect the push notification to a DIDcomm message",
    )
    recipient_key = fields.Str(
        # TODO: add
    )
