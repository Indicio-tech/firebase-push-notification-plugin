from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)

from ..messages.set_device_info import SetDeviceInfo
from ..models.device_record import DeviceRecord


class SetDeviceInfoHandler(BaseHandler):
    """Handler class for setting device info."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle setting device info.

        Args:
            context: Request context
            responder: Responder callback
        """
        
        self._logger.debug(f"SetDeviceInfoHandler called with context {context}")
        assert isinstance(context.message, SetDeviceInfo)

        device_record = DeviceRecord(
            device_token=context.message.device_token,
        )

        async with context.profile.session() as session:
            await device_record.save(
                session,
                reason="Save device info"
            )
