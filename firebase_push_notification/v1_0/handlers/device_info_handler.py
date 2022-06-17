from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)

from ..messages.device_info import DeviceInfo


class DeviceInfoHandler(BaseHandler):
    """Handler class for device info."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle device info.

        Args:
            context: Request context
            responder: Responder callback
        """

        self._logger.debug(f"DeviceInfoHandler called with context {context}")
        assert isinstance(context.message, DeviceInfo)