import logging
from re import L

from aries_cloudagent.connections.base_manager import BaseConnectionManager
from aries_cloudagent.core.profile import Profile
from aries_cloudagent.messaging.responder import BaseResponder

from .messages.set_device_info import SetDeviceInfo
from .messages.device_info import DeviceInfo


class PushNotificationManager(BaseConnectionManager):
    """Class for managing push notifications."""

    def __init__(self, profile: Profile):
        """
        Initialize a PushNotificationManager.

        Args:
            profile: The profile for this connection manager
        """
        self._profile = profile
        self._logger = logging.getLogger(__name__)
        super().__init__(self._profile)

    async def send_device_info(self, get_device_info: SetDeviceInfo):

        device_info = DeviceInfo()
        device_info.assign_thread_id(get_device_info.thread_id)

        responder = self._profile.inject_or(BaseResponder)
        if responder:
            await responder.send_reply(
                device_info,
            )