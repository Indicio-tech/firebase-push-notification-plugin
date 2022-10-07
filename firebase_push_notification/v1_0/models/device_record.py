from marshmallow import fields

from aries_cloudagent.messaging.models.base_record import BaseRecord, BaseRecordSchema
from aries_cloudagent.core.profile import ProfileSession


class DeviceRecord(BaseRecord):
    """Represents device information."""

    class Meta:
        """DeviceRecord metadata."""

        schema_class = "DeviceRecordSchema"

    RECORD_TYPE = "device_record"
    RECORD_TOPIC = "device_topic"
    TAG_NAMES = {"device_token", "connection_id"}
    CONNECTION_ID = "connection_id"

    def __init__(
        self,
        device_token=None,
        connection_id=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.device_token = device_token
        self.connection_id = connection_id

    @classmethod
    async def query_by_connection_id(cls, session: ProfileSession, connection_id: str):

        tag_filter = {"connection_id": connection_id}
        return await cls.retrieve_by_tag_filter(session, tag_filter)


class DeviceRecordSchema(BaseRecordSchema):
    class Meta:
        """DeviceRecordSchema metadata"""

        model_class = DeviceRecord

    device_token = fields.Str(
        required=True,
        description="The token that is required by the notification provider",
    )
    connection_id = fields.Str(
        required=True, description="The connection_id of the undeliverable message"
    )
