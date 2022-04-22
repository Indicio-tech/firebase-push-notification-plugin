import logging

from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)

from ..messages.device_info import DeviceInfo
from ..messages.get_device_info import GetDeviceInfo
from ..models.device_record import DeviceRecord

LOGGER = logging.getLogger(__name__)


class GetDeviceInfoHandler(BaseHandler):
    """Handler class for getting device info."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle getting device info.

        Args:
            context: Request context
            responder: Responder callback
        """

        self._logger.debug(f"GetDeviceInfoHandler called with context {context}")
        assert isinstance(context.message, GetDeviceInfo)

        device_info = await self.get_device_info_handler(context)
        device_info.assign_thread_from(context.message)
        await responder.send_reply(device_info)

    async def get_device_info_handler(self, context: RequestContext):
        session = await context.session()
        records = await DeviceRecord.query(session, {})
        device_info = DeviceInfo(device_token=records[0].device_token)

        return device_info