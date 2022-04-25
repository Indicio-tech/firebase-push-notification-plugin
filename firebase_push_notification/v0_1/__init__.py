"""ACA-Py Event to firebase Bridge."""

import logging
import re
from typing import Optional, cast

from aries_cloudagent.core.event_bus import Event, EventBus, EventWithMetadata
from aries_cloudagent.core.profile import Profile
from aries_cloudagent.core.util import SHUTDOWN_EVENT_PATTERN, STARTUP_EVENT_PATTERN
from aries_cloudagent.config.injection_context import InjectionContext

LOGGER = logging.getLogger(__name__)


async def setup(context: InjectionContext):
    """Setup the plugin."""
    
    bus = context.inject(EventBus)
    if not bus:
        raise ValueError("EventBus missing in context")

    LOGGER.info("subscribing to events for firebase.")
    bus.subscribe(re.compile(re.compile(".*")), handle_event)

    bus.subscribe(STARTUP_EVENT_PATTERN, on_startup)
    bus.subscribe(SHUTDOWN_EVENT_PATTERN, on_shutdown)


RECORD_RE = re.compile(r"acapy::record::([^:]*)(?:::(.*))?")
WEBHOOK_RE = re.compile(r"acapy::webhook::{.*}")


async def on_startup(profile: Profile, event: Event):
    LOGGER.info("Starting Firebase!")
    # config = get_config(profile.settings).events or EventsConfig.default()
    # start firebase producer
    #producer = #firebase(**config.producer.dict())
    #profile.context.injector.bind_instance(Firebaseporducer, producer)
    #await producer.start()


async def on_shutdown(profile: Profile, event: Event):
    LOGGER.info("shuting down firebase!")
    # kill firebase producer


def _derive_category(topic: str):
    match = RECORD_RE.match(topic)
    if match:
        return match.group(1)
    if WEBHOOK_RE.match(topic):
        return "webhook"


async def handle_event(profile: Profile, event: EventWithMetadata):
    """Produce firebase events from aca-py events."""
    #producer = profile.inject(FirebaseProducer)

    LOGGER.info("Handling producer event: %s", event)
    wallet_id = cast(Optional[str], profile.settings.get("wallet.id"))
    payload = {
        "wallet_id": wallet_id or "base",
        "state": event.payload.get("state"),
        "topic": event.topic,
        "category": _derive_category(event.topic),
        "payload": event.payload,
    }
    try:
        LOGGER.info(f"Sending notification {payload}.")
        # await producer.send_and_wait(
        #    _topic,
        #    str.encode(json.dumps(payload)),
        #    key=wallet_id.encode() if wallet_id else None,
        #)
    except Exception:
        LOGGER.exception("producer failed to send notification")