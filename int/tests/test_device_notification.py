import pytest
import logging
import os
import re

from aries_cloudagent.core.event_bus import EventBus, Event, MockEventBus

from .firebase_push_notification.v1_0.routes import register_events, firebase_push_notification_handler
from .firebase_push_notification.v1_0.models.device_record import DeviceRecord


LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_set_device_info(echo, echo_connection):
    """Test for setting device info. SetDeviceInfo message responds
    with DeviceInfo message."""

    device_token = os.getenv("FIREBASE_DEVICE_TOKEN_INT_TESTS")
    
    async with echo.session(echo_connection) as session:
        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/set-device-info",
                "device_token": device_token,
            },
        )

        device_info = await echo.get_message(
            echo_connection,
            session=session,
            msg_type=(
                "https://didcomm.org/push-notifications-fcm-android/1.0/device-info"
            )
        )

    assert device_info["device_token"] == device_token



@pytest.mark.asyncio
async def test_get_device_info(echo, echo_connection):
    """Test for setting and getting device info.GetDeviceInfo message responds
    with DeviceInfo message."""

    device_token = os.getenv("FIREBASE_DEVICE_TOKEN_INT_TESTS")

    async with echo.session(echo_connection) as session:
        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/set-device-info",
                "device_token": device_token,
            },
        )

        await echo.get_message(
            echo_connection,
            session=session,
            msg_type=(
                "https://didcomm.org/push-notifications-fcm-android/1.0/device-info"
            )
        )

        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/get-device-info",
                "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            }
        )

        device_info = await echo.get_message(
            echo_connection,
            session=session,
            msg_type=(
                "https://didcomm.org/push-notifications-fcm-android/1.0/device-info"
            )
        )

    assert device_info["device_token"] == device_token



@pytest.mark.asyncio
async def test_push_notification(echo, echo_connection):
    """"Test for sending push notification and receiving push
    notification acknowledgement"""

    device_token = os.getenv("FIREBASE_DEVICE_TOKEN_INT_TESTS")
    
    async with echo.session(echo_connection) as session:
        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/set-device-info",
                "device_token": device_token,
            },
        )

        await echo.get_message(
            echo_connection,
            session=session,
            msg_type=(
                "https://didcomm.org/push-notifications-fcm-android/1.0/device-info"
            )
        )

    async with echo.session(echo_connection) as session:

        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/push-notification",
                "message_id": "message_id_placeholder",
                "recipient_key": "recipient_key_placeholder"
            },
        )

        await echo.get_message(
            echo_connection,
            session=session,
            msg_type=(
                "https://didcomm.org/push-notifications-fcm-android/1.0/push-notification-ack"
            )
        )


@pytest.mark.asyncio
async def test_firebase_push_notification_handler(event_bus, profile):
    # Create device record
    device_record = DeviceRecord(
        device_token = os.getenv("FIREBASE_DEVICE_TOKEN_INT_TESTS"),
        connection_id = "connection-1"
    )
    # Save device record
    async with profile.session() as session:
        await device_record.save(
            session,
            reason="Save device info"
        )

    # Trigger push notification handler
    topic = "acapy::outbound_message::undeliverable"
    payload = {
        "connection_id": "connection-1",
        "message_id": "test id",
        "content": "Hello world",
        "state": "received",
        }
    event = Event(topic, payload)
    register_events(event_bus)
    await firebase_push_notification_handler(profile, event)
    # await event_bus.notify(profile, event)
