from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)
from aries_cloudagent.protocols.coordinate_mediation.v1_0.models.mediation_record import MediationRecord

from ..messages.set_device_info import SetDeviceInfo
from ..messages.device_info import DeviceInfo
from ..models.device_record import DeviceRecord


class SetDeviceInfoHandler(BaseHandler):
    """Handler class for setting device info."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handler setting device info. Responds with DeviceInfo message.

        Args:
            context: Request context
            responder: Responder callback
        """
        
        self._logger.debug(f"SetDeviceInfoHandler called with context {context}")
        assert isinstance(context.message, SetDeviceInfo)

        device_info = await self.set_device_info_handler(
            context,
            device_token=context.message.device_token,
            connection_id=context.connection_record.connection_id,
            )
        device_info.assign_thread_from(context.message)
        await responder.send_reply(device_info)

    async def set_device_info_handler(self, context: RequestContext, device_token, connection_id):
        """
        Create and save DeviceRecord, create and return DeviceInfo
        """
        device_record = DeviceRecord(
            device_token=device_token,
            connection_id=connection_id,
        )

        async with context.profile.session() as session:
            await device_record.save(
                session,
                reason="Save device info"
            )

            records = await DeviceRecord.query(session, {})
            device_info = DeviceInfo(device_token=records[0].device_token)
        
        return device_info

    async def verify_mediated_connection(self, context: RequestContext, connection_id):
        """
        Verify that the connection between agent and relay/mediator is mediated.
        """
        session = await context.session()
        mediation_record = await MediationRecord.retrieve_by_connection_id(session, connection_id)
        assert mediation_record.state == "granted"

        return mediation_record