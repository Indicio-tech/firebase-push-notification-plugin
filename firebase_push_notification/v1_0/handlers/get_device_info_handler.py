import logging

from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)

from ..messages.get_device_info import GetDeviceInfo
from ..manager import PushNotificationManager

LOGGER = logging.getLogger(__name__)


class GetDeviceInfoHandler(BaseHandler):
    """Handler class for getting device info."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle connection invitation.

        Args:
            context: Request context
            responder: Responder callback
        """
        profile = context.profile
        LOGGER.debug("GetDeviceInfoHandler: %s", context.message_delivery.message_id)
        self._logger.debug(f"GetDeviceInfoHandler called with context {context}")
        assert isinstance(context.message, GetDeviceInfo)

        credential_manager = PushNotificationManager(profile)
        get_device_info = GetDeviceInfo()
        credential_manager.send_device_info(get_device_info)


        # TODO: add problem report
        # report = ConnectionProblemReport(
        #     problem_code=ProblemReportReason.INVITATION_NOT_ACCEPTED,
        #     explain="Connection invitations cannot be submitted via agent messaging",
        # )
        # # client likely needs to be using direct responses to receive the problem report
        # await responder.send_reply(report)


