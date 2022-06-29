import json
import logging
from typing import Optional

import requests
from aries_cloudagent.messaging.base_handler import (BaseHandler,
                                                     BaseResponder,
                                                     RequestContext)

from ..messages.push_notification import PushNotification
from ..messages.push_notification_ack import PushNotificationAck

LOGGER = logging.getLogger(__name__)


class PushNotificationHandler(BaseHandler):
    """Handler class for push notification."""

    def __init__(
        self,
        *,
        device_token: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.device_token = device_token

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Handle push notification.

        Args:
            context: Request context
            responder: Responder callback
        """

        self._logger.debug(f"PushNotificationHandler called with context {context}")
        assert isinstance(context.message, PushNotification)
        LOGGER.info("Firebase push notification")
        configs = context.profile.settings["plugin_config"].get("firebase_plugin", {}) # possible bug with incorrect profile
        firebase_server_token = configs.get("firebase_server_token")
        if not self.device_token:
            self.device_token = configs.get("device_token")

        # TODO: lookup from device registry using recipient key
        payload = {
            "message_id": context.message.message_id
        }
        headers = {"Content-Type": "application/json", "Authorization": f"key={firebase_server_token}"}
        body = {
            "notification": {
                "title": "Sending push notification from ACA-Py",
                "body": "Test push notification",
            },
            "to": self.device_token,
            "priority": context.message.priority,
            "data": payload,
        }
        LOGGER.info(f"Push notification handler body {body}")
        LOGGER.info(f"Push notification handler headers {headers}")
        response = requests.post(
            "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body)
        )
        LOGGER.info(f"Push notification response {response}.")
        try:
            LOGGER.info(f"In handler sending firebase notification {payload}.")
        except Exception:
            LOGGER.exception("Firebase producer failed to send notification")

        push_notification_ack = PushNotificationAck()
        push_notification_ack.assign_thread_from(context.message)
        await responder.send_reply(push_notification_ack)
