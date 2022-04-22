"""Firebase Push Notification Plugin"""

import logging

from aries_cloudagent.config.injection_context import InjectionContext

LOGGER = logging.getLogger(__name__)

__all__ = ["FirebasePushNotificationPlugin"]


async def setup(context: InjectionContext):
    """Setup the plugin."""
    LOGGER.warning("Welcome to the firebase push notification plugin.")
