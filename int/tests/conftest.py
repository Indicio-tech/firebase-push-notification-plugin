"""Common fixtures for testing."""

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

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def event_loop():
    """Create a session scoped event loop.
    pytest.asyncio plugin provides a default function scoped event loop
    which cannot be used as a dependency to session scoped fixtures.
    """
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def host():
    """Hostname of agent under test."""
    return os.environ.get("AGENT_HOST", "localhost")


@pytest.fixture(scope="session")
def suite_host():
    """Hostname of agent under test."""
    return os.environ.get("SUITE_HOST", "localhost")


@pytest.fixture(scope="session")
def suite_port():
    """Port of agent under test."""
    return os.environ.get("SUITE_PORT", 3002)


@pytest.fixture(scope="session")
def backchannel_port():
    """Port of agent under test backchannel."""
    return os.environ.get("AGENT_BACKCHANNEL_PORT", 3001)


@pytest.fixture(scope="session")
def backchannel(host, backchannel_port):
    """Yield backchannel client."""
    yield Client(base_url="http://{}:{}".format(host, backchannel_port))


@pytest.fixture(scope="session")
def suite_seed():
    yield hashlib.sha256(b"acapy-plugin-toolbox-int-test-runner").hexdigest()[:32]


@pytest.fixture(scope="session")
def agent_seed():
    yield hashlib.sha256(b"acapy-plugin-toolbox-int-test-runner").hexdigest()[:32]


@pytest.fixture(scope="session")
def suite_endpoint():
    yield os.environ.get("SUITE_ENDPOINT", "http://localhost:3000")


@pytest.fixture(scope="session")
def agent_connection(
    suite_seed, agent_seed, suite_endpoint, backchannel
) -> Iterator[ConnectionStaticResult]:
    """Yield agent's representation of this connection."""

    # Create connection in agent under test
    create_result: Optional[ConnectionStaticResult] = create_static.sync(
        client=backchannel,
        json_body=ConnectionStaticRequest.from_dict(
            {
                "my_seed": agent_seed,
                "their_seed": suite_seed,
                "their_endpoint": suite_endpoint,
                "their_label": "test-runner",
            }
        ),
    )
    if not create_result:
        raise RuntimeError("Could not create static connection with agent under test")

    # Set admin metadata to enable access to admin protocols
    set_result = set_metadata.sync(
        client=backchannel,
        conn_id=create_result.record.connection_id,
        json_body=ConnectionMetadataSetRequest.from_dict(
            {"metadata": {"group": "admin"}}
        ),
    )
    if not set_result:
        raise RuntimeError("Could not set metadata on static connection")

    yield create_result

    delete_connection.sync(
        client=backchannel, conn_id=create_result.record.connection_id
    )


@pytest.fixture(scope="session")
def echo_agent(suite_host, suite_port):
    yield EchoClient(base_url=f"http://{suite_host}:{suite_port}")


@pytest.fixture
async def echo(echo_agent: EchoClient):
    async with echo_agent:
        yield echo_agent


@pytest.fixture(scope="session")
async def echo_connection(echo_agent: EchoClient, suite_seed, agent_connection):
    async with echo_agent:
        conn = await echo_agent.new_connection(
            seed=suite_seed,
            endpoint="ws://agent:3003",  # TODO: ENV
            their_vk=agent_connection.my_verkey,
        )
    yield conn
    async with echo_agent:
        await echo_agent.delete_connection(conn)


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
