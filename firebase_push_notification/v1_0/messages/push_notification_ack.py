from marshmallow import EXCLUDE

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema

from ..message_types import PUSH_NOTIFICATION_ACK


class PushNotificationAck(AgentMessage):

    class Meta:
        """Metadata for push notifications"""

        message_type = PUSH_NOTIFICATION_ACK
        schema_class = "PushNotificationAckSchema"

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)


class PushNotificationAckSchema(AgentMessageSchema):
    """Push notification schema class."""

    class Meta:
        """Push notification schema metadata."""

        model_class = PushNotificationAck
        unknown = EXCLUDE