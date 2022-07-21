from marshmallow import fields, EXCLUDE

from ..message_types import PUSH_NOTIFICATION

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema


class PushNotification(AgentMessage):

    class Meta:
        """Metadata for push notifications"""

        message_type = PUSH_NOTIFICATION
        schema_class = "PushNotificationSchema"

    def __init__(
        self,
        *,
        message_id: str = None,
        message_tag: str = None,
        recipient_key: str = None,
        priority: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.message_id = message_id
        self.message_tag = message_tag
        self.recipient_key = recipient_key
        self.priority = priority


class PushNotificationSchema(AgentMessageSchema):
    """Push notification schema class."""

    class Meta:
        """Push notification schema metadata."""

        model_class = PushNotification
        unknown = EXCLUDE

    message_id = fields.Str(
        required=False,
        description="Optional field to connect the push notification to a DIDcomm message",
    )
    message_tag = fields.Str(
        required=False,
        description="Optional field to connect the push notification to a DIDcomm message",
    )
    recipient_key = fields.Str(
        required=True,
        description="Optional field for recipient key",
    )
    priority = fields.Str(
        required=False,
        default="high",
        description="Optional field for priority of message",
    )
