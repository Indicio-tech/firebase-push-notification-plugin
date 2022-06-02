import pytest
import logging
import asyncio

from echo_agent import EchoClient

LOGGER = logging.getLogger(__name__)



##############################################

# import pyyaml module
import yaml
from yaml.loader import SafeLoader

# Open the file and load the file
with open('plugin-config.yml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    device_token = data["device_token"]

##############################################



@pytest.fixture(scope="session")
def event_loop():
    """Create a session scoped event loop.
    pytest.asyncio plugin provides a default function scoped event loop
    which cannot be used as a dependency to session scoped fixtures.
    """
    return asyncio.get_event_loop()

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
            endpoint=agent_connection.my_endpoint,
            their_vk=agent_connection.my_verkey,
        )
    yield conn
    async with echo_agent:
        await echo_agent.delete_connection(conn)


@pytest.mark.asyncio
async def test_set_device_info():
    async with echo.session(echo_connection) as session:
        await echo.send_message_to_session(
            session,
            {
                "@type": "https://didcomm.org/push-notifications-fcm-android/1.0/set-device-info",
                "device_token": device_token,
            },
        )
