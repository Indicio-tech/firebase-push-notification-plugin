from marshmallow import fields, EXCLUDE

from ..message_types import PROTOCOL, SET_DEVICE_INFO

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema


HANDLER_CLASS = "firebase_push_notification.v0_1.handlers.set_device_info_handler.SetDeviceInfoHandler"


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
