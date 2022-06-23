import json
import logging
from typing import Optional, cast

import requests
from aries_cloudagent.messaging.base_handler import (BaseHandler,
                                                     BaseResponder,
                                                     RequestContext)

from ..messages.push_notification import PushNotification
from ..messages.push_notification_ack import PushNotificationAck

LOGGER = logging.getLogger(__name__)

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
        #send push notification to fb for device
        LOGGER.info("Firebase push notification")
        configs = context.profile.settings["plugin_config"].get("firebase_plugin", {}) # possible bug with incorrect profile
        firebase_server_token = configs.get("firebase_server_token")
        device_token = configs.get("device_token")
        headers = {"Content-Type": "application/json", "Authorization": f"key={firebase_server_token}"}
        body = {
            "notification": {
                "title": "Sending push notification from ACA-Py",
                "body": "Test push notification",
            },
            "to": device_token,
            "priority": "high",
            "data": {},
        }
        response = requests.post(
            "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body)
        )
        try:
            LOGGER.info(f"Sending firebase notification {{}}.")
        except Exception:
            LOGGER.exception("Firebase producer failed to send notification")

        push_notification_ack = PushNotificationAck()
        push_notification_ack.assign_thread_from(context.message)
        await responder.send_reply(push_notification_ack)
