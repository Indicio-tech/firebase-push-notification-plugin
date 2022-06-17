from aries_cloudagent.messaging.base_handler import (
    BaseHandler,
    BaseResponder,
    RequestContext,
)

from ..messages.push_notification import PushNotification
from ..messages.push_notification_ack import PushNotificationAck


class PushNotificationHandler(BaseHandler):
    """Handler class for push notification."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle push notification.

        Args:
            context: Request context
            responder: Responder callback
        """

        self._logger.debug(f"PushNotificationHandler called with context {context}")
        assert isinstance(context.message, PushNotification)

        push_notification_ack = PushNotificationAck()
        push_notification_ack.assign_thread_from(context.message)
        await responder.send_reply(push_notification_ack)