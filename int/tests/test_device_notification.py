import pytest
import logging

LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_set_get_device_info(echo, echo_connection):
    """Test for setting and getting device info"""

    device_token = "device_token_placeholder"

    async with echo.session(echo_connection) as session:
        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/set-device-info",
                "device_token": device_token,
            },
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

    async with echo.session(echo_connection) as session:

        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/push-notification",
                "message_tag": "message_tag_placeholder",
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