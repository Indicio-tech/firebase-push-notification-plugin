""" Message Type Identifiers for Push Notifications """
from aries_cloudagent.protocols.didcomm_prefix import DIDCommPrefix


SPEC_URI = "https://didcomm.org/push-notifications-fcm/1.0"

PROTOCOL_PACKAGE = "firebase_push_notification.v1_0"

SET_DEVICE_INFO = f"{SPEC_URI}/set-device-info"
GET_DEVICE_INFO = f"{SPEC_URI}/get-device-info"
DEVICE_INFO = f"{SPEC_URI}/device-info"
PUSH_NOTIFICATION = f"{SPEC_URI}/push-notification"

MESSAGE_TYPES = DIDCommPrefix.qualify_all(
    {
        SET_DEVICE_INFO: f"{PROTOCOL_PACKAGE}.messages.set_device_info.SetDeviceInfo",
        GET_DEVICE_INFO: f"{PROTOCOL_PACKAGE}.messages.get_device_info.GetDeviceInfo",
        DEVICE_INFO: f"{PROTOCOL_PACKAGE}.messages.device_info.DeviceInfo",
        PUSH_NOTIFICATION: f"{PROTOCOL_PACKAGE}.messages.push_notification.PushNotification",
    }
)