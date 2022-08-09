import pytest

from aries_cloudagent.core.event_bus import EventBus
from aries_cloudagent.core.in_memory import InMemoryProfile
from aries_cloudagent.messaging.responder import BaseResponder, MockResponder
from aries_cloudagent.core.protocol_registry import ProtocolRegistry


@pytest.fixture
def event_bus():
    """Event bus fixture."""
    yield EventBus()


@pytest.fixture
def mock_responder():
    """Mock responder fixture."""
    yield MockResponder()


@pytest.fixture
def profile(event_bus, mock_responder):
    """Profile fixture."""
    yield InMemoryProfile.test_profile(
        bind={
            EventBus: event_bus,
            BaseResponder: mock_responder,
            ProtocolRegistry: ProtocolRegistry(),
        }
    )
