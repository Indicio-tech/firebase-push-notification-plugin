from marshmallow import fields, EXCLUDE

from ..message_types import PROTOCOL, PUSH_NOTIFICATION

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema


HANDLER_CLASS = "firebase_push_notification.v0_1.handlers.push_notification_handler.PushNotificationHandler"


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
