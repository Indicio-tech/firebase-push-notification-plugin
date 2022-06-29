import logging
import re
import requests
import json
from typing import Optional, cast
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

LOGGER = logging.getLogger(__name__)


def register_events(event_bus: EventBus):
    """Register to handle events."""
    LOGGER.info("Firebase, subscribe to all events!")
    event_bus.subscribe(re.compile(re.compile(".*")), handle_event)


RECORD_RE = re.compile(r"acapy::record::([^:]*)(?:::(.*))?")
WEBHOOK_RE = re.compile(r"acapy::webhook::{.*}")


async def on_startup(profile: Profile, event: Event):
    LOGGER.info("Starting Firebase!")


async def on_shutdown(profile: Profile, event: Event):
    LOGGER.info("shuting down firebase!")


def _derive_category(topic: str):
    match = RECORD_RE.match(topic)
    if match:
        return match.group(1)
    if WEBHOOK_RE.match(topic):
        return "webhook"


async def handle_event(profile: Profile, event: EventWithMetadata):
    """Produce firebase events from aca-py events."""
    LOGGER.info("Firebase push notification")
    configs = profile.settings["plugin_config"].get("firebase_plugin", {})
    firebase_server_token = configs.get("firebase_server_token")
    device_token = configs.get("device_token")
    wallet_id = cast(Optional[str], profile.settings.get("wallet.id"))
    payload = {
        "wallet_id": wallet_id or "base",
        "state": event.payload.get("state"),
        "topic": event.topic,
        "category": _derive_category(event.topic),
        "payload": event.payload,
    }
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
        "data": payload,
    }
    LOGGER.info(f"Routes body {body}")
    LOGGER.info(f"Routes headers {headers}")
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body)
    )
    try:
        LOGGER.info(f"In routes sending firebase notification {payload}.")
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