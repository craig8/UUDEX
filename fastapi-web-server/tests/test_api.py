import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from typing import AsyncGenerator

from uudex_server import get_settings
from uudex_server.main import app    # Assuming main.py where FastAPI instance is created

# Replace 'sqlite:///:memory:' with your actual database URL if required
DATABASE_URL = 'sqlite:///:memory:'


@pytest.fixture(scope="module")
async def async_client(setup_test_env) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_root(async_client: AsyncClient) -> None:
    response = await async_client.get("/")
    assert response.status_code == 200


def test_api_get_all_participants(test_client: TestClient):
    response = test_client.get("/participants/")
    assert response.status_code == 200


def test_api_get_participant_by_id(test_client: TestClient):
    response = test_client.get("/participant/1")
    assert response.status_code == 200


def test_api_get_endpoint_user(test_client: TestClient):
    response = test_client.get("/endpoint/me")
    assert response.status_code == 200


def test_api_get_all_subjects(test_client: TestClient):
    response = test_client.get("/subjects/")
    assert response.status_code == 200


def test_api_get_subject_by_id(test_client: TestClient):
    response = test_client.get("/subject/1")
    assert response.status_code == 200


def test_api_create_subject(test_client: TestClient):
    data = {
        "subject_uuid": "uuid1",
        "subject_name": "name1",
        "dataset_instance_key": "key1",
        "subscription_type": "sub_type1",
        "fulfillment_types_available": "fulfillment1",
        "full_queue_behavior": "behavior1",
        "max_queue_size_kb": 1000,
        "max_message_count": 10,
        "priority": 1,
        "backing_exchange_name": "exchange1",
        "owner_participant_id": 1,
        "dataset_definition_id": 1,
    }
    response = test_client.post("/subjects/", json=data)
    assert response.status_code == 200


def test_api_get_all_subscriptions(test_client: TestClient):
    response = test_client.get("/subscriptions/")
    assert response.status_code == 200


def test_api_get_subscription_by_id(test_client: TestClient):
    response = test_client.get("/subscription/uuid1")
    assert response.status_code == 200


def test_api_create_subscription(test_client: TestClient):
    data = {
        "subscription_uuid": "uuid1",
        "subscription_name": "name1",
        "subscription_state": "active"
    }
    response = test_client.post("/subscription/", json=data)
    assert response.status_code == 200


# Run the tests
if __name__ == '__main__':
    pytest.main()
