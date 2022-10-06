import json
import logging
import os
import re
from typing import cast

import requests
from aiohttp import web
from aiohttp_apispec import docs, match_info_schema, response_schema
from aries_cloudagent.admin.request_context import AdminRequestContext
from aries_cloudagent.core.event_bus import EventBus, EventWithMetadata
from aries_cloudagent.core.profile import Profile
from aries_cloudagent.messaging.models.openapi import OpenAPISchema
from aries_cloudagent.messaging.valid import UUIDFour
from aries_cloudagent.transport.outbound.message import OutboundMessage
from marshmallow import fields

from .handlers.set_device_info_handler import SetDeviceInfoHandler
from .messages.push_notification import PushNotification
from .models.device_record import DeviceRecord

LOGGER = logging.getLogger(__name__)


class RegisterDeviceTokenSchema(OpenAPISchema):
    """Result schema for mediation list query."""

    device_token = fields.Str(
        required=True,
        description="The token that is required by the notification provider",
    )
    connection_id = fields.UUID(
        description="Connection identifier (optional)",
        required=False,
        example=UUIDFour.EXAMPLE,
    )


class ResponseDeviceInfoSchema(OpenAPISchema):
    device_token = fields.Str(
        required=True,
        description="The token that is required by the notification provider",
    )


UNDELIVERABLE_RE = re.compile(r"acapy::outbound-message::undeliverable")


def register_events(event_bus: EventBus):
    """Register to handle events."""
    LOGGER.info("Firebase, subscribe to all events!")
    event_bus.subscribe(UNDELIVERABLE_RE, firebase_push_notification_handler)


def push_notifications(event, firebase_server_token, device_token):
    """Construct and post push notification message"""
    assert firebase_server_token
    assert device_token
    push_notification: PushNotification = PushNotification(
        message_id="placeholder_msg_id",
        message_tag="placeholder_msg_tag",
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"key={firebase_server_token}",
    }

    body = {
        "to": device_token,
        "priority": "high",
        "data": push_notification.serialize(),
        "content_available": True,
    }
    LOGGER.info(f"Body {body}")
    LOGGER.info(f"Headers {headers}")
    try:
        LOGGER.info(f"In routes sending firebase notification {push_notification}.")
        return requests.post(
            "https://fcm.googleapis.com/fcm/send",
            headers=headers,
            data=json.dumps(body),
        )

    except Exception:
        LOGGER.exception("Firebase producer failed to send notification")


async def firebase_push_notification_handler(
    profile: Profile, event: EventWithMetadata
):
    """Produce firebase events from aca-py events."""
    LOGGER.info("Firebase push notification")

    plugin_config = profile.settings["plugin_config"] or {}
    config = plugin_config["firebase"]
    env_firebase_server_token = os.getenv("FIREBASE_SERVER_TOKEN")
    firebase_server_token = config.get("server_token", env_firebase_server_token)
    assert firebase_server_token

    # Retrieve the connection_id of the undeliverable message from the event payload
    outbound = cast(OutboundMessage, event.payload)
    connection_id = outbound.connection_id
    # TODO: look up connection id based on reply to verkey
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
            push_notifications(event, firebase_server_token, device_token)


@docs(
    tags=["pushnotification"],
    summary="Manually add a device token to a mediated connection",
)
@match_info_schema(RegisterDeviceTokenSchema())
@response_schema(ResponseDeviceInfoSchema(), 200, description="")
async def register_device_token(request: web.BaseRequest):
    device_token = request.match_info["device_token"]
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
            web.post(
                "/push-notification/register/{device_token}/{connection_id}",
                register_device_token,
            )
        ]
    )
