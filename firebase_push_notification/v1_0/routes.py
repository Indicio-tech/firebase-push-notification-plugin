import logging
import re
import os
import requests
import json

from aries_cloudagent.core.event_bus import EventBus, EventWithMetadata
from aries_cloudagent.core.profile import Profile

from .messages.push_notification import PushNotification
from .models.device_record import DeviceRecord

LOGGER = logging.getLogger(__name__)

UNDELIVERABLE_RE = re.compile(r"acapy::outbound_message::undeliverable")

def register_events(event_bus: EventBus):
    """Register to handle events."""
    LOGGER.info("Firebase, subscribe to all events!")
    event_bus.subscribe(UNDELIVERABLE_RE, firebase_push_notification_handler)


async def firebase_push_notification_handler(profile: Profile, event: EventWithMetadata):
    """Produce firebase events from aca-py events."""
    LOGGER.info("Firebase push notification")
    device_token = os.getenv("FIREBASE_DEVICE_TOKEN_INT_TESTS")
    firebase_server_token = os.getenv("FIREBASE_SERVER_TOKEN")
    assert device_token
    assert firebase_server_token

    # Retrieve the connection_id of the undeliverable message from the event payload
    connection_id = event.payload.get("connection_id")
    LOGGER.info(f"Connection_id: {connection_id}")

    # Use the connection_id to query the device records
    async with profile.session() as session:
        results = await DeviceRecord.query_by_connection_id(
            session=session,
            connection_id=connection_id,
        )
        LOGGER.info(f"Query results: {results}")

        # Retrieve the device_token associated with the connection_id
        if results:
            device_token = results.device_token
        # TODO: anticipate collisions

        push_notification = PushNotification(
            message_id=event.payload.get("message_id"),
            message_tag=event.payload.get("message_tag"),
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": "key=" + firebase_server_token,
        }
        body = {
            "notification": {
                "title": "Sending push notification from ACA-Py",
                "body": "Test push notification",
            },
            "to": device_token,
            "priority": "high",
            "data": push_notification.serialize(),
        }
        LOGGER.info(f"Body {body}")
        LOGGER.info(f"Headers {headers}")

        response = requests.post(
            "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body)
        )
        try:
            LOGGER.info(f"In routes sending firebase notification {push_notification}.")
        except Exception:
            LOGGER.exception("Firebase producer failed to send notification")