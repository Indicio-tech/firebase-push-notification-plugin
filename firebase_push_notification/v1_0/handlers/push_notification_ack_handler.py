from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)

from ..messages.push_notification_ack import PushNotificationAck


class PushNotificationAckHandler(BaseHandler):
    """Handler class for push notification acknowledgement."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle push notification acknowledgement.

        Args:
            context: Request context
            responder: Responder callback
        """

        self._logger.debug(f"PushNotificationAckHandler called with context {context}")
        assert isinstance(context.message, PushNotificationAck)