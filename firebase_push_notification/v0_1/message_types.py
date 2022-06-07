""" Message Type Identifiers for Push Notifications """
from aries_cloudagent.protocols.didcomm_prefix import DIDCommPrefix


PROTOCOL = "https://didcomm.org/push-notifications-fcm-android/1.0"

PROTOCOL_PACKAGE = "firebase_push_notification.v0_1.message"


# Message types
SET_DEVICE_INFO = f"{PROTOCOL}/set-device-info"  # register device?
GET_DEVICE_INFO = f"{PROTOCOL}/get-device-info"  # offer notification config?
DEVICE_INFO = f"{PROTOCOL}/device-info"
PUSH_NOTIFICATION = f"{PROTOCOL}/push-notification"


MESSAGE_TYPES = DIDCommPrefix.qualify_all(
    {
        SET_DEVICE_INFO: f"{PROTOCOL_PACKAGE}.SetDeviceInfo",
        GET_DEVICE_INFO: f"{PROTOCOL_PACKAGE}.GetDeviceInfo",
        DEVICE_INFO: f"{PROTOCOL_PACKAGE}.DeviceInfo",
        PUSH_NOTIFICATION: f"{PROTOCOL_PACKAGE}.PushNotification",
    }
)
