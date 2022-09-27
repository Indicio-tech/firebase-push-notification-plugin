import pytest
import logging
import os

LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_set_device_info(echo, echo_connection):
    """Test for setting device info. SetDeviceInfo message responds
    with DeviceInfo message."""

    device_token = os.getenv("DEVICE_TOKEN")

    async with echo.session(echo_connection) as session:
        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm/1.0/set-device-info",
                "device_token": device_token,
            },
        )

        device_info = await echo.get_message(
            echo_connection,
            session=session,
            msg_type=("https://didcomm.org/push-notifications-fcm/1.0/device-info"),
        )

    assert device_info["device_token"] == device_token


@pytest.mark.asyncio
async def test_get_device_info(echo, echo_connection):
    """Test for setting and getting device info.GetDeviceInfo message responds
    with DeviceInfo message."""

    device_token = os.getenv("DEVICE_TOKEN")

    async with echo.session(echo_connection) as session:
        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm/1.0/set-device-info",
                "device_token": device_token,
            },
        )

        await echo.get_message(
            echo_connection,
            session=session,
            msg_type=("https://didcomm.org/push-notifications-fcm/1.0/device-info"),
        )

        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm/1.0/get-device-info",
                "thread_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            },
        )

        device_info = await echo.get_message(
            echo_connection,
            session=session,
            msg_type=("https://didcomm.org/push-notifications-fcm/1.0/device-info"),
        )

    assert device_info["device_token"] == device_token
