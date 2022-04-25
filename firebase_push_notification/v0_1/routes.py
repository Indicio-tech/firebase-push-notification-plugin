import re

from typing import Sequence

from aries_cloudagent.core.event_bus import Event, EventBus
from aries_cloudagent.core.profile import Profile, ProfileSession
from aries_cloudagent.connections.models.conn_record import ConnRecord
from aries_cloudagent.messaging.agent_message import AgentMessage
from aries_cloudagent.messaging.responder import BaseResponder
from aries_cloudagent.protocols.connections.v1_0.manager import ConnectionManager

import logging

LOGGER = logging.getLogger(__name__)

def register_events(event_bus: EventBus):
    """Register to handle events."""
    LOGGER.info("subscribe to all events!")
    event_bus.subscribe(
        re.compile(f".*"),
        firebase_push_notification,
    )


async def firebase_push_notification(profile: Profile, event: Event):
    LOGGER.info("Firebase push notification")
    # TODO: write