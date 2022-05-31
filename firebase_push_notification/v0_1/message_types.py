""" Message Type Identifiers for Push Notifications """
from aries_cloudagent.protocols.didcomm_prefix import DIDCommPrefix


PROTOCOL = "https://didcomm.org/push-notifications-fcm-android/1.0"

PROTOCOL_PACKAGE = "firebase_push_notification.v0_1"


SET_DEVICE_INFO = f"{PROTOCOL}/set-device-info"  # register device?
GET_DEVICE_INFO = f"{PROTOCOL}/get-device-info"  # offer notification config?
DEVICE_INFO = f"{PROTOCOL}/device-info"
PUSH_NOTIFICATION = f"{PROTOCOL}/push-notification"


MESSAGE_TYPES = DIDCommPrefix.qualify_all(
    {
        SET_DEVICE_INFO: "push_notifications_native.SetDeviceInfo",
        GET_DEVICE_INFO: "push_notifications_native.GetDeviceInfo.",
        DEVICE_INFO: "push_notifications_native.DeviceInfo.",
        PUSH_NOTIFICATION: "push_notifications_native.PushNotification",
    }
)
