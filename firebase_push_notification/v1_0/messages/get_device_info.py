from marshmallow import EXCLUDE, fields

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema

from ..message_types import GET_DEVICE_INFO


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
