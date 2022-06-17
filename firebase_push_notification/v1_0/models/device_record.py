from marshmallow import fields

from aries_cloudagent.messaging.models.base_record import BaseRecord, BaseRecordSchema


class DeviceRecord(BaseRecord):
    """Represents device information."""

    class Meta:
        """DeviceRecord metadata."""

        schema_class = "DeviceRecordSchema"

    RECORD_TYPE = "device_record"
    RECORD_TOPIC = "device_topic"
    TAG_NAMES = {"device_token"}
    
    def __init__(
        self,
        device_token = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.device_token = device_token


class DeviceRecordSchema(BaseRecordSchema):

    class Meta:
        """DeviceRecordSchema metadata"""

        model_class = DeviceRecord

    device_token = fields.Str(
        required=True, description="The token that is required by the notification provider"
    )