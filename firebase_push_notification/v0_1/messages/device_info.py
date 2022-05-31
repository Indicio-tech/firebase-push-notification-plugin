from marshmallow import fields, pre_dump, ValidationError, EXCLUDE

from ..message_types import PROTOCOL, DEVICE_INFO

from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema


HANDLER_CLASS = f"{PROTOCOL}.handlers.device_info_handler.DeviceInfoHandler"


class DeviceInfo(AgentMessage):
    """Class for device info."""

    class Meta:
        """Metadata for device info."""

        handler_class = HANDLER_CLASS
        message_type = DEVICE_INFO
        schema_class = "DeviceInfoSchema"

    def __init__(
        self,
        *,
        device_token: str = None,
        thid: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.device_token = device_token
        self.thid = thid


class DeviceInfoSchema(AgentMessageSchema):
    """Device info schema class."""

    class Meta:
        """Device info schema metadata."""

        model_class = DeviceInfo
        unknown = EXCLUDE

    device_token = fields.Str(
        required=True,
        description="The token that is required by the notification provider",
    )
    thid = fields.Str(
        required=False,
        description="GetDeviceInfo UUID",
    )

    @pre_dump
    def check_thread_deco(self, obj, **kwargs):
        """Thread decorator, and its thid and pthid, are mandatory."""
        if not obj._decorators.to_dict().get("~thread", {}).keys() >= {
            "thid"
        }:  # pthid is not required for notification
            raise ValidationError("Missing required field(s) in thread decorator")
        return obj
