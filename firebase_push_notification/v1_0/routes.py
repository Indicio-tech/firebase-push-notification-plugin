import logging
import re
import os
import requests
import json
from aiohttp import web
from aiohttp_apispec import (
    docs,
    response_schema,
    match_info_schema,
)
from marshmallow import fields

from aries_cloudagent.core.event_bus import EventBus, EventWithMetadata
from aries_cloudagent.core.profile import Profile
from aries_cloudagent.admin.request_context import AdminRequestContext
from aries_cloudagent.messaging.models.openapi import OpenAPISchema
from aries_cloudagent.messaging.valid import UUIDFour

from .messages.push_notification import PushNotification
from .models.device_record import DeviceRecord
from .handlers.set_device_info_handler import SetDeviceInfoHandler


LOGGER = logging.getLogger(__name__)


class RegisterDeviceTokenSchema(OpenAPISchema):
    """Result schema for mediation list query."""
    device_token = fields.Str(
        required=True,
        description="The token that is required by the notification provider"
    )
    connection_id =  fields.UUID(
        description="Connection identifier (optional)",
        required=False,
        example=UUIDFour.EXAMPLE,
    )


class ResponseDeviceInfoSchema(OpenAPISchema):
    device_token = fields.Str(
        required=True,
        description="The token that is required by the notification provider",
    )


UNDELIVERABLE_RE = re.compile(r"acapy::outbound_message::undeliverable")
FORWARD_RE = re.compile(r"acapy::forward::received")


def register_events(event_bus: EventBus):
    """Register to handle events."""
    LOGGER.info("Firebase, subscribe to all events!")
    event_bus.subscribe(UNDELIVERABLE_RE, firebase_push_notification_handler)
    event_bus.subscribe(FORWARD_RE, firebase_push_notification_handler)
    # event_bus.subscribe(re.compile(re.compile(".*")), handle_event)


async def firebase_push_notification_handler(profile: Profile, event: EventWithMetadata):
    """Produce firebase events from aca-py events."""
    LOGGER.info("Firebase push notification")

    firebase_server_token = os.getenv("FIREBASE_SERVER_TOKEN")
    assert firebase_server_token

    # Retrieve the connection_id of the undeliverable message from the event payload
    connection_id = event.payload.get("connection_id")
    LOGGER.info(f"Connection_id: {connection_id}")

    # Use the connection_id to query the device records
    async with profile.session() as session:
        results = await DeviceRecord.query_by_connection_id(
            session=session,
            connection_id=connection_id,
        )
        LOGGER.info(f"Query results: {results}")

        # Retrieve the device_token associated with the connection_id
        if results:
            device_token = results.device_token
            # TODO: anticipate collisions
            assert device_token
        push_notification = PushNotification(
            message_id=event.payload.get("message_id"),
            message_tag=event.payload.get("message_tag"),
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": "key=" + firebase_server_token,
        }
        body = {
            "notification": {
                "title": "Sending push notification from ACA-Py",
                "body": "Test push notification",
            },
            "to": device_token,
            "priority": "high",
            "data": push_notification.serialize(),
        }
        LOGGER.info(f"Body {body}")
        LOGGER.info(f"Headers {headers}")

        response = requests.post(
            "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body)
        )
        try:
            LOGGER.info(f"In routes sending firebase notification {push_notification}.")
        except Exception:
            LOGGER.exception("Firebase producer failed to send notification")



async def handle_event(profile: Profile, event: EventWithMetadata):
    """
    Proof of concept for manual testing.

    Produce firebase events from aca-py events."""
    LOGGER.info("Firebase push notification")
    configs = profile.settings["plugin_config"].get("firebase_plugin", {})
    firebase_server_token = configs.get("firebase_server_token")
    device_token = configs.get("device_token")
    payload = {
        "payload": event.payload,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "key=" + firebase_server_token,
    }
    body = {
        "notification": {
            "title": "Sending push notification from ACA-Py",
            "body": "Test push notification",
        },
        "to": device_token,
        "priority": "high",
        "data": payload,
    }
    LOGGER.info(f"Routes body {body}")
    LOGGER.info(f"Routes headers {headers}")
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body)
    )
    try:
        LOGGER.info(f"In routes sending firebase notification {payload}.")
    except Exception:
        LOGGER.exception("Firebase producer failed to send notification")


@docs(
    tags=["pushnotification"],
    summary="Manually add a device token to a mediated connection",
)
@match_info_schema(RegisterDeviceTokenSchema())
@response_schema(ResponseDeviceInfoSchema(), 200, description="")
async def register_device_token(request: web.BaseRequest):
    device_token=request.match_info["device_token"]
    connection_id = request.match_info["connection_id"]

    handler = SetDeviceInfoHandler()
    context: AdminRequestContext = request["context"]

    # verify that connnection is mediated
    await handler.verify_mediated_connection(context, connection_id)

    device_info = await handler.set_device_info_handler(
        context=context,
        device_token=device_token,
        connection_id=connection_id,
    )
    return web.json_response({"device_token": device_info.device_token})


async def register(app: web.Application):
    app.add_routes(
        [
            web.post("/push-notification/{device_token}/{connection_id}", register_device_token),
        ]
    )