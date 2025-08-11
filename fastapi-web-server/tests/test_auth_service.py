"""
Test the authentication service database access
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from uudex_server.services.authentication_service import AuthenticationService
from uudex_server.services.database_service import get_db_session
from uudex_server.core.settings import get_settings


@pytest.mark.asyncio
async def test_authentication_service_database_access():
    """Test that the authentication service can access the database"""

    # Get settings and create auth service
    settings = get_settings()
    auth_service = AuthenticationService.create(settings)

    # Test with a mock certificate DN
    test_dn = "test_user"

    # Use the database session
    async with get_db_session() as db_session:
        # This should return None for a non-existent certificate but not crash
        endpoint = await auth_service.get_endpoint_by_certificate_dn(test_dn, db_session)

        # We expect None since we don't have test data, but the important thing is no exceptions
        assert endpoint is None

        print("✅ Authentication service database access test passed!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_authentication_service_database_access())
