import pytest
from fastapi.testclient import TestClient
from uudex_api_mock_server import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_server(client):
    """Reset server state before each test"""
    client.post("/mock/reset")


def test_subscription_operations(client):
    # Create subscription
    subscription_data = {
        "id": "sub1",
        "subject_id": "subject1",
        "callback_url": "http://example.com/callback",
    }

    response = client.post("/api/v1/subscriptions", json=subscription_data)
    assert response.status_code == 200
    assert response.json() == subscription_data

    # Get subscriptions
    response = client.get("/api/v1/subscriptions")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == subscription_data

    # Delete subscription
    response = client.delete("/api/v1/subscriptions/sub1")
    assert response.status_code == 200

    # Verify deletion
    response = client.get("/api/v1/subscriptions")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_message_operations(client):
    # Publish message
    message_data = {"content": "test message", "metadata": {"key": "value"}}

    response = client.post("/api/v1/subjects/subject1/messages", json=message_data)
    assert response.status_code == 200
    assert "message_id" in response.json()

    # Get messages
    response = client.get("/api/v1/subjects/subject1/messages")
    assert response.status_code == 200
    assert len(response.json()) == 1
    message = response.json()[0]
    assert message["content"] == "test message"
    assert message["metadata"] == {"key": "value"}


def test_configure_custom_response(client):
    # Configure custom response
    mock_config = {
        "path": "/api/v1/custom",
        "response": {"message": "Custom response"},
        "status_code": 200,
    }

    response = client.post("/mock/configure", json=mock_config)
    assert response.status_code == 200

    # Test custom endpoint
    response = client.get("/api/v1/custom")
    assert response.status_code == 200
    assert response.json() == {"message": "Custom response"}


def test_request_history(client):
    # Make some requests
    client.get("/api/v1/subscriptions")
    client.post("/api/v1/subscriptions", json={"id": "test"})

    # Check history
    response = client.get("/mock/history")
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 2
    assert history[0]["path"] == "/api/v1/subscriptions"
    assert history[0]["method"] == "GET"
    assert history[1]["path"] == "/api/v1/subscriptions"
    assert history[1]["method"] == "POST"
    assert history[1]["body"] == {"id": "test"}


def test_configure_and_use_mock(client):
    # Configure mock response
    mock_config = {
        "path": "/api/test",
        "response": {"message": "Hello, World!"},
        "status_code": 200,
    }

    response = client.post("/mock/configure", json=mock_config)
    assert response.status_code == 200

    # Test configured endpoint
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

    # Check request history
    history = client.get("/mock/history")
    assert history.status_code == 200
    history_data = history.json()
    assert len(history_data) == 1  # only the test request
    assert history_data[0]["path"] == "/api/test"


def test_unconfigured_path_returns_404(client):
    response = client.get("/api/undefined")
    assert response.status_code == 404


def test_error_response(client):
    # Configure error response
    mock_config = {
        "path": "/api/error",
        "response": {"detail": {"error": "Bad Request"}},
        "status_code": 400,
    }

    client.post("/mock/configure", json=mock_config)

    response = client.get("/api/error")
    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "Bad Request"
