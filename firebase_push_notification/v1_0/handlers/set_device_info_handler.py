from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)
from aries_cloudagent.core.event_bus import Event
from aries_cloudagent.core.profile import ProfileSession

from ..messages.set_device_info import SetDeviceInfo
from ..models.device_record import DeviceRecord


class SetDeviceInfoHandler(BaseHandler):
    """Handler class for setting device info."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle connection invitation.

        Args:
            context: Request context
            responder: Responder callback
        """
        
        self._logger.debug(f"SetDeviceInfoHandler called with context {context}")
        assert isinstance(context.message, SetDeviceInfo)

        device_record = DeviceRecord(
            device_token=context.message.device_token,
        )
        self._logger.debug(f"device record! {device_record}")
        self._logger.debug(f"context.message! {context.message}")

        async with context.profile.session() as session:
            await device_record.save(
                session,
                reason="Save device info"
            )
        
        # TODO: add problem report

        # report = ConnectionProblemReport(
        #     problem_code=ProblemReportReason.INVITATION_NOT_ACCEPTED,
        #     explain="Connection invitations cannot be submitted via agent messaging",
        # )
        # # client likely needs to be using direct responses to receive the problem report
        # await responder.send_reply(report)
