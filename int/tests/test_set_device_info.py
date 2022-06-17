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

    # get device info
    async with echo.session(echo_connection) as session:
        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/get-device-info",
            }
        )
    LOGGER.info("Get-device-info!")
    device_info = await echo.get_messages(echo_connection)
    LOGGER.info(device_info)
    # retrieve device info message
    device_info = await echo.get_message(
        echo_connection,
        session=session,
        msg_type=(
            "https://didcomm.org/push-notifications-fcm-android/1.0/device-info"
        )
    )
    assert device_info["device_token"] == device_token



# @pytest.mark.asyncio
# async def test_push_notification(echo, echo_connection):

#     async with echo.session(echo_connection) as session:
#         await echo.send_message_to_session(
#             session,
#             {
#                 "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/push-notification",
#                 "message_tag": "message_tag_placeholder",
#                 "recipient_key": "recipient_key_placeholder"
#             },
#         )
#     # TODO: assert that message was received?