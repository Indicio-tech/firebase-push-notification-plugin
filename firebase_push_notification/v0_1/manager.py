import logging

from aries_cloudagent.connections.base_manager import BaseConnectionManager
from aries_cloudagent.core.profile import Profile


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
