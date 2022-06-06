import pytest
import logging

from echo_agent import EchoClient

LOGGER = logging.getLogger(__name__)


##############################################
# # # import pyyaml module
# import yaml
# from yaml.loader import SafeLoader

# # Open the file and load the file
# with open('plugin-config.yml') as f:
#     data = yaml.load(f, Loader=SafeLoader)
#     device_token = data["device_token"]

device_token = "cYHSGX-GSGanrP2msvHVti:APA91bHruQ6SVOoyESgdHQsJE2xbNyf3mWq9spEXbzHtbiv9jcs-ZE2ojC2KXc4Rbdt8ej9RXiYqasTLRP67IGy2rki1gT-JJBad4IxeIzkWgs6duNAHqFOwadTfI2fsBfZFKQe6PzrH"
##############################################


@pytest.mark.asyncio
async def test_set_get_device_info(echo, echo_connection):
    
    # set device info
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
                "@type": "https://didcomm.org/push-notifications-apns/1.0/get-device-info",
            }
        )

    # retrieve device info message
    device_info = await echo.get_message(
        echo_connection,
        session=session,
        msg_type=(
            "https://didcomm.org/push-notifications-apns/1.0/get-device-info"
        )
    )
    assert device_info["device_token"] == device_token


@pytest.mark.asyncio
async def test_push_notification(echo, echo_connection):

    async with echo.session(echo_connection) as session:
        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/push-notification",
                "message_tag": "message_tag_placeholder",
                "recipient_key": "recipient_key_placeholder"
            },
        )
