import pytest
import logging
from asynctest import mock
import os

from aries_cloudagent.core.event_bus import EventBus, Event

from firebase_push_notification.v1_0.routes import register_events
from firebase_push_notification.v1_0.models.device_record import DeviceRecord
from aries_cloudagent.transport.outbound.message import OutboundMessage


LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_firebase_push_notification_handler(profile, event_bus: EventBus):
    # Create device record
    device_record = DeviceRecord(
        device_token=os.getenv("DEVICE_TOKEN"), connection_id="connection-1"
    )

    # Save device record
    async with profile.session() as session:
        await device_record.save(session, reason="Save device info")
    assert device_record.device_token != "device_token_placeholder"

    # Trigger push notification handler
    payload = OutboundMessage(payload="payload", connection_id="connection-1")
    topic = "acapy::outbound-message::undeliverable"
    event = Event(topic, payload)
    register_events(event_bus)

    with mock.patch("requests.post") as m:
        await event_bus.notify(profile, event)
        m.assert_called_once()
