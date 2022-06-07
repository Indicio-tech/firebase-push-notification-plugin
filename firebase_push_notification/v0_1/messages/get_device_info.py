from marshmallow import EXCLUDE

from ..message_types import PROTOCOL, GET_DEVICE_INFO

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema


HANDLER_CLASS = "firebase_push_notification.v0_1.handlers.get_device_info_handler.GetDeviceInfoHandler"


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
        **kwargs,
    ):
        super().__init__(**kwargs)


class GetDeviceInfoSchema(AgentMessageSchema):
    """Get device info schema class."""

    class Meta:
        """Get device info schema metadata."""

        model_class = GetDeviceInfo
        unknown = EXCLUDE

