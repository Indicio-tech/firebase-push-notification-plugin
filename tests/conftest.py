import pytest

import asyncio
import hashlib
import logging
import os
from typing import Iterator, Optional

from acapy_client import Client
from acapy_client.api.connection import (
    create_static,
    delete_connection,
    set_metadata,
)
from acapy_client.models import (
    ConnectionMetadataSetRequest,
    ConnectionStaticRequest,
    ConnectionStaticResult,
)
from echo_agent import EchoClient
import pytest

from aries_cloudagent.core.event_bus import EventBus, Event, MockEventBus
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