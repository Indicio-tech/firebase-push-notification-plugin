import logging
import re
import os
import requests
import json
from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)

from aries_cloudagent.core.event_bus import Event, EventBus, EventWithMetadata
from aries_cloudagent.core.profile import Profile
from aries_cloudagent.messaging.responder import BaseResponder
from aries_cloudagent.messaging.request_context import RequestContext
from aries_cloudagent.admin.request_context import AdminRequestContext

from .messages.push_notification import PushNotificationSchema
from .messages.push_notification_ack import PushNotificationAckSchema
from .messages.push_notification import PushNotification
from .handlers.push_notification_handler import PushNotificationHandler
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
            "data": push_notification,
        }
        LOGGER.info(f"Body {body}")
        LOGGER.info(f"Headers {headers}")
        response = requests.post(
            "https://fcm.googleapis.com/fcm/send", headers=headers, data=body  # previously json.dumps(body)
        )
        try:
            LOGGER.info(f"In routes sending firebase notification {push_notification}.")
        except Exception:
            LOGGER.exception("Firebase producer failed to send notification")



async def register(app: web.Application):
    app.add_routes(
        [
            web.post("/push-notification/{firebase_server_token}{device_token}", push_notification),
        ]
    )


@docs(
    tags=["pushnotification"],
    summary="Send a push notification",
)
@request_schema(PushNotificationSchema())
@response_schema(PushNotificationAckSchema(), 200, description="")
async def push_notification(request: web.BaseRequest):

    body = await request.json()
    handler = PushNotificationHandler(
        device_token = body.get("device_token")
    )

    context: AdminRequestContext = request["context"]
    profile = context.profile
    request_context = RequestContext(profile=profile)
    request_context.message = PushNotification(
        message_id="placeholder",
        recipient_key="placeholder",
        priority="default",
    )
    responder = context.injector.inject(BaseResponder)

    await handler.handle(
        context=request_context,
        responder=responder
    )

    return web.json_response()