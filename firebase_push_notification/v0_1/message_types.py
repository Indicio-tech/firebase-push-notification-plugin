""" Message Type Identifiers for Push Notifications """
from aries_cloudagent.protocols.didcomm_prefix import DIDCommPrefix


SPEC_URI = "https://didcomm.org/push-notifications-fcm-android/1.0"

PROTOCOL = "firebase-push-notification"
VERSION = "1.0"
BASE = f"{PROTOCOL}/{VERSION}"

PROTOCOL_PACKAGE = "firebase_push_notification.v0_1"

# Message types
SET_DEVICE_INFO = f"{SPEC_URI}/set-device-info"  # register device?
GET_DEVICE_INFO = f"{SPEC_URI}/get-device-info"  # offer notification config?
DEVICE_INFO = f"{SPEC_URI}/device-info"
PUSH_NOTIFICATION = f"{SPEC_URI}/push-notification"

MESSAGE_TYPES = DIDCommPrefix.qualify_all(
    {
        SET_DEVICE_INFO: f"{PROTOCOL_PACKAGE}.messages.SetDeviceInfo",
        GET_DEVICE_INFO: f"{PROTOCOL_PACKAGE}.messages.GetDeviceInfo",
        DEVICE_INFO: f"{PROTOCOL_PACKAGE}.messages.DeviceInfo",
        PUSH_NOTIFICATION: f"{PROTOCOL_PACKAGE}.messages.PushNotification",
    }
)
