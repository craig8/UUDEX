import pytest
import pytest_asyncio
import os
from typing import AsyncGenerator, Dict, Any
import uvicorn
import asyncio
import threading
from fastapi.testclient import TestClient
from uudex_api_mock_server import app as mock_app
import httpx
import json
from pathlib import Path


class ServerThread(threading.Thread):

    def __init__(self, host: str = "127.0.0.1", port: int = 8004):
        super().__init__()
        self.host = host
        self.port = port
        self.should_exit = threading.Event()

    def run(self):
        config = uvicorn.Config(mock_app,
                                host=self.host,
                                port=self.port,
                                log_level="error")
        self.server = uvicorn.Server(config)
        self.server.run()

    def stop(self):
        self.should_exit.set()
        self.server.should_exit = True


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def mock_server(event_loop):
    """Start mock server in a separate thread"""
    server = ServerThread()
    server.daemon = True
    server.start()
    # Give the server a moment to start
    event_loop.run_until_complete(asyncio.sleep(0.1))
    yield server
    server.stop()


class UUDEXTestClient:
    """Test client for UUDEX API"""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(base_url=base_url)
        # Test participant credentials
        self.app_rt_id = "4b3b819e-94bd-4adf-b461-17ccb58ac870"
        self.mitre_client_id = "8f026ebe-c71e-4fa1-8d66-82d3d85b72a4"

    async def configure_mock(self,
                             path: str,
                             response: dict,
                             status_code: int = 200):
        """Configure mock response"""
        path = path.lstrip('/')
        response = await self.client.post("/mock/configure",
                                          json={
                                              "path": path,
                                              "response": response,
                                              "status_code": status_code
                                          })
        response.raise_for_status()

    async def get_participants(self):
        """Get all participants"""
        response = await self.client.get("api/v1/participants")
        response.raise_for_status()
        return response.json()

    async def get_participant(self, participant_id: str):
        """Get specific participant"""
        response = await self.client.get(
            f"api/v1/participants/{participant_id}")
        response.raise_for_status()
        return response.json()

    async def get_subjects(self):
        """Get all subjects"""
        response = await self.client.get("api/v1/subjects")
        response.raise_for_status()
        return response.json()

    async def get_subject(self, subject_id: str):
        """Get specific subject"""
        response = await self.client.get(f"api/v1/subjects/{subject_id}")
        response.raise_for_status()
        return response.json()

    async def create_subscription(self,
                                  subject_id: str,
                                  callback_url: str,
                                  participant_id: str = None):
        """Create a subscription"""
        if participant_id is None:
            participant_id = self.app_rt_id

        response = await self.client.post("api/v1/subscriptions",
                                          json={
                                              "subject_id": subject_id,
                                              "participant_id": participant_id,
                                              "callback_url": callback_url
                                          })
        response.raise_for_status()
        return response.json()

    async def get_subscriptions(self, participant_id: str = None):
        """Get all subscriptions for a participant"""
        url = "api/v1/subscriptions"
        if participant_id:
            url += f"?participant_id={participant_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def publish_message(self, subject_id: str, message: Dict[str, Any]):
        """Publish message to a subject"""
        response = await self.client.post(
            f"api/v1/subjects/{subject_id}/messages", json=message)
        response.raise_for_status()
        return response.json()

    async def get_messages(self, subject_id: str):
        """Get messages for a subject"""
        response = await self.client.get(
            f"api/v1/subjects/{subject_id}/messages")
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()


@pytest_asyncio.fixture
async def api_client(mock_server) -> AsyncGenerator:
    """Create UUDEX API client configured for mock server"""
    base_url = os.getenv("UUDEX_API_URL", "http://localhost:8004")
    client = UUDEXTestClient(base_url=base_url)

    # Reset mock server state before each test
    async with httpx.AsyncClient() as http_client:
        await http_client.post(f"{base_url}/mock/reset")

        # Load fixture data
        fixtures_path = Path(__file__).parent / "fixtures" / "mock_data.json"
        with open(fixtures_path) as f:
            mock_data = json.load(f)

        # Configure initial state
        for endpoint, data in {
                "api/v1/participants": mock_data["participants"],
                "api/v1/subjects": mock_data["subjects"],
                "api/v1/subscriptions": mock_data["subscriptions"]
        }.items():
            await http_client.post(f"{base_url}/mock/configure",
                                   json={
                                       "path": endpoint,
                                       "response": data,
                                       "status_code": 200
                                   })

    yield client
    await client.close()


@pytest.mark.asyncio
async def test_get_participants(api_client):
    """Test getting all participants"""
    participants = await api_client.get_participants()
    assert len(participants) == 2
    participant_ids = {p["participant_id"] for p in participants}
    assert api_client.app_rt_id in participant_ids
    assert api_client.mitre_client_id in participant_ids


@pytest.mark.asyncio
async def test_get_subjects(api_client):
    """Test getting all subjects"""
    subjects = await api_client.get_subjects()
    assert len(subjects) == 2
    subject_ids = {s["subject_id"] for s in subjects}
    assert "test/mitre/1" in subject_ids
    assert "test/app_rt/1" in subject_ids


@pytest.mark.asyncio
async def test_subscriptions_workflow(api_client):
    """Test subscription creation and retrieval"""
    # Create new subscription
    new_sub = await api_client.create_subscription(
        subject_id="test/mitre/1",
        callback_url="https://new-app.example.com/callback")
    assert new_sub["subject_id"] == "test/mitre/1"

    # Get subscriptions
    subs = await api_client.get_subscriptions(
        participant_id=api_client.app_rt_id)
    assert len(subs) >= 1
    assert any(s["subject_id"] == "test/mitre/1" for s in subs)


@pytest.mark.asyncio
async def test_message_workflow(api_client):
    """Test message publishing and retrieval"""
    # Publish message
    message = {"message": "Test message"}
    result = await api_client.publish_message("test/mitre/1", message)
    assert "message_id" in result

    # Get messages
    messages = await api_client.get_messages("test/mitre/1")
    assert len(messages) >= 1
    assert any(m["content"]["message"] == "Test message" for m in messages)


@pytest.mark.asyncio
async def test_mock_configuration(api_client):
    """Test mock server configuration"""
    # Configure custom response
    custom_response = {
        "participant_id": "custom-id",
        "participant_name": "Custom Participant"
    }
    await api_client.configure_mock("api/v1/participants/custom-id",
                                    custom_response)

    # Verify custom response
    response = await api_client.client.get("api/v1/participants/custom-id")
    assert response.status_code == 200
    assert response.json() == custom_response
