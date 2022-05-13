import re
import logging
from typing import Optional
import cast
from marshmallow import fields

from aries_cloudagent.core.event_bus import Event, EventBus
from aries_cloudagent.core.profile import Profile
from aries_cloudagent.core.util import SHUTDOWN_EVENT_PATTERN, STARTUP_EVENT_PATTERN
from aries_cloudagent.core.profile import InjectionContext, Profile
from aries_cloudagent.core.protocol_registry import ProtocolRegistry
from aries_cloudagent.core.event_bus import Event, EventBus
from aries_cloudagent.protocols.problem_report.v1_0.message import ProblemReport

from .util import generate_model_schema
from .routes import (
    on_startup,
    on_shutdown,
    handle_event)

LOGGER = logging.getLogger(__name__)


PROTOCOL = (
    "https://didcomm.org/push-notifications-fcm-android/1.0"
)

SET_DEVICE_INFO = f"{PROTOCOL}/set-device-info"  # register device?
GET_DEVICE_INFO = f"{PROTOCOL}/get-device-info"  # offer notification config?
DEVICE_INFO = f"{PROTOCOL}/device-info"

MESSAGE_TYPES = {
    SET_DEVICE_INFO: "push_notifications_native.SetDeviceInfo",
    GET_DEVICE_INFO: "push_notifications_native.GetDeviceInfo.",
    DEVICE_INFO: "push_notifications_native.DeviceInfo.",
}



async def setup(context: InjectionContext):
    """Setup the plugin."""
    config = get_config(context.settings).events
    if not config:
        config = EventsConfig.default()

    bus = context.inject(EventBus)
    if not bus:
        raise ValueError("EventBus missing in context")

    for event in config.topic_maps.keys():
        LOGGER.info(f"subscribing to event: {event}")
        bus.subscribe(re.compile(event), handle_event)

    bus.subscribe(STARTUP_EVENT_PATTERN, on_startup)
    bus.subscribe(SHUTDOWN_EVENT_PATTERN, on_shutdown)



SetDeviceInfo, SetDeviceInfoSchema = generate_model_schema(
    name="SetDeviceInfo",
    handler="push_notifications_native.util.PassHandler",
    msg_type=SET_DEVICE_INFO,
    schema={
        "@type": fields.Str,
        # "@id": fields.Str,
        "device_token": fields.Str,
        # "device_platform": fields.Str,
    },
)


GetDeviceInfo, GetDeviceInfoSchema = generate_model_schema(
    name="GetDeviceInfo",
    handler="push_notifications_native.util.PassHandler",
    msg_type=GET_DEVICE_INFO,
    schema={
        "@type": fields.Str,
        # "@id": fields.Str,
        "sender_id": fields.Str,
    },
)


DeviceInfo, DeviceInfoSchema = generate_model_schema(
    name="DeviceInfo",
    handler="push_notifications_native.util.PassHandler",
    msg_type=DEVICE_INFO,
    schema={
        "@type": fields.Str,
        "device_token": fields.Str,
        "device_platform": fields.Str,
        "~thread": fields.Dict,
    },
)