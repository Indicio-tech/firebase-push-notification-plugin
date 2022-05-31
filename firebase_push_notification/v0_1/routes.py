import logging
import re
import requests
import json
from typing import Optional, cast

from aries_cloudagent.connections.models.conn_record import ConnRecord
from aries_cloudagent.core.event_bus import Event, EventBus, EventWithMetadata
from aries_cloudagent.core.profile import Profile, ProfileSession
from aries_cloudagent.core.util import SHUTDOWN_EVENT_PATTERN, STARTUP_EVENT_PATTERN
from aries_cloudagent.messaging.agent_message import AgentMessage
from aries_cloudagent.messaging.responder import BaseResponder
from aries_cloudagent.protocols.connections.v1_0.manager import ConnectionManager

LOGGER = logging.getLogger(__name__)


def register_events(event_bus: EventBus):
    """Register to handle events."""
    LOGGER.info("Firebase, subscribe to all events!")
    event_bus.subscribe(re.compile(re.compile(".*")), handle_event)
    event_bus.subscribe(STARTUP_EVENT_PATTERN, on_startup)
    event_bus.subscribe(SHUTDOWN_EVENT_PATTERN, on_shutdown)


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
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body)
    )
    try:
        LOGGER.info(f"Sending firebase notification {payload}.")
    except Exception:
        LOGGER.exception("Firebase producer failed to send notification")
