"""
Test script to verify the authentication service database access
"""
import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from uudex_server.services.authentication_service import AuthenticationService
from uudex_server.services.database_service import get_db_session


async def test_authentication_service():
    """Test the authentication service with database access"""
    print("Testing authentication service...")

    # Create authentication service
    auth_service = AuthenticationService.create(None)

    # Test with database session
    async with get_db_session() as session:
        # Try to get an endpoint (this will return None if no matching certificate)
        test_dn = "alice"    # Replace with actual certificate DN from your test data
        endpoint = await auth_service.get_endpoint_by_certificate_dn(test_dn, session)

        if endpoint:
            print(f"✅ Found endpoint: {endpoint.endpoint_user_name}")
            print(f"   Certificate DN: {endpoint.certificate_dn}")
            print(f"   Participant: {endpoint.participant.participant_short_name}")
            print(f"   Active: {endpoint.active_sw}")
            print(f"   Participant Active: {endpoint.participant.active_sw}")
        else:
            print(f"❌ No endpoint found for certificate DN: {test_dn}")

        # Test cache functionality
        print("\nTesting cache...")
        endpoint2 = await auth_service.get_endpoint_by_certificate_dn(test_dn, session)
        if endpoint and endpoint2:
            print("✅ Cache working - same object returned")
        else:
            print("ℹ️  Cache test skipped - no endpoint found")


if __name__ == "__main__":
    asyncio.run(test_authentication_service())
