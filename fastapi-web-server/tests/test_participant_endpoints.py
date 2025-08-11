import pytest
from uuid import uuid4
from httpx import AsyncClient

# Use full path imports to be explicit
from uudex_server.models.common_types import YNSwitch
from uudex_server.models import Participant, ParticipantCreate


@pytest.mark.asyncio
async def test_list_participants(client: AsyncClient, admin_headers):
    """Test listing participants"""
    response = await client.get("/participants/", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_participant_crud(client: AsyncClient, admin_headers):
    """Test participant CRUD operations"""
    # Create
    create_data = {
        "participant_uuid": "test-uuid",
        "participant_short_name": "test",
        "participant_long_name": "Test Participant",
        "description": "Test description",
        "root_org_sw": "Y",
        "active_sw": "Y"
    }
    response = await client.post("/participants/", json=create_data, headers=admin_headers)
    assert response.status_code == 200
    created = response.json()
    participant_id = created["participant_id"]

    # Read
    response = await client.get(f"/participant/{participant_id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["participant_uuid"] == "test-uuid"

    # Update
    update_data = {"participant_short_name": "updated", "description": "Updated description"}
    response = await client.put(f"/participant/{participant_id}",
                                json=update_data,
                                headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated description"

    # Delete
    response = await client.delete(f"/participant/{participant_id}", headers=admin_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_participant_validation(client: AsyncClient, admin_headers):
    """Test participant validation"""
    invalid_data = {
        "participant_uuid": "",    # Empty UUID
        "participant_short_name": "x" * 51,    # Too long
        "root_org_sw": "INVALID"    # Invalid Y/N value
    }
    response = await client.post("/participants/", json=invalid_data, headers=admin_headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_participant_permissions(client: AsyncClient, admin_headers, non_admin_headers,
                                       missing_cert_headers):
    """Test participant endpoint permissions"""
    # Admin can access
    response = await client.get("/participants/", headers=admin_headers)
    assert response.status_code == 200

    # Non-admin access is restricted
    response = await client.get("/participants/", headers=non_admin_headers)
    assert response.status_code in (401, 403)

    # Missing cert is rejected
    response = await client.get("/participants/", headers=missing_cert_headers)
    assert response.status_code == 401
