#!/usr/bin/env python3
"""
Simple HTTP client to test UUDEX endpoints using httpx (no generated client needed).
This tests the FastAPI endpoints directly with certificate simulation.
"""

import sys
import asyncio
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    import httpx
    from uudex_server.main import app
    from uudex_server.services.database_service import init_db
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this from the fastapi-web-server directory")
    sys.exit(1)


def simulate_certificate_headers(cert_name="alice"):
    """
    Return headers that simulate what Caddy would send for certificate authentication.
    """
    # Map cert names to their actual certificate CNs
    cert_subjects = {
        "alice": "CN=3fa9be8b-a0f9-40a5-ab3d-51d580d4797e_alice,O=Acme Corp,C=US",
        "pnnl": "CN=0a476033-5cc6-4050-a289-ddf11a8fe0d4-pnnl-client,O=PNNL,C=US",
        "acme": "CN=fb9afb6d-566-ACME-Publisher,O=ACME Publisher,C=US"
    }

    subject = cert_subjects.get(cert_name, cert_subjects["alice"])

    return {
        "X-Client-Cert-Subject": subject,
        "X-Client-Cert-Issuer": "CN=LocalCA,O=Test CA,C=US",
        "X-Client-Cert-Serial": "123456789"
    }


async def test_endpoints_with_httpx():
    """
    Test UUDEX endpoints using httpx directly.
    """
    print("UUDEX HTTP Test with httpx")
    print("=" * 40)

    # Test different certificates
    test_certs = ["alice", "pnnl", "acme"]

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:

        for cert_name in test_certs:
            print(f"\n--- Testing with {cert_name} certificate ---")

            # Get certificate headers
            headers = simulate_certificate_headers(cert_name)
            print(f"Subject: {headers['X-Client-Cert-Subject']}")

            try:
                # Test basic root endpoint
                response = await client.get("/", headers=headers)
                print(f"✅ Root endpoint: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    cert_info = data.get("certificate_info", {})
                    print(f"   Detected CN: {cert_info.get('cn', 'Not found')}")

                # Test endpoint/me
                response = await client.get("/endpoint/me", headers=headers)
                print(f"Endpoint/me: {response.status_code}")

                if response.status_code == 200:
                    endpoint_data = response.json()
                    print(
                        f"✅ Authenticated as: {endpoint_data.get('endpoint_user_name', 'Unknown')}"
                    )
                    print(f"   Endpoint ID: {endpoint_data.get('endpoint_id', 'Unknown')}")
                elif response.status_code == 401:
                    print("❌ Authentication failed - certificate not in database")
                else:
                    print(f"❌ Unexpected response: {response.text[:100]}...")

                # Test subjects endpoint
                print("Testing subjects endpoints...")

                # Try get all subjects
                response = await client.get("/subjects/", headers=headers)
                print(f"GET /subjects/: {response.status_code}")

                if response.status_code == 200:
                    subjects = response.json()
                    print(f"✅ Found {len(subjects)} subjects")
                    for i, subject in enumerate(subjects[:3], 1):    # Show first 3
                        if isinstance(subject, dict):
                            name = subject.get('subject_name', 'Unknown')
                            subject_id = subject.get('subject_id', 'N/A')
                            print(f"   {i}. {name} (ID: {subject_id})")
                        else:
                            print(f"   {i}. {subject}")
                    if len(subjects) > 3:
                        print(f"   ... and {len(subjects) - 3} more")
                elif response.status_code == 401:
                    print("❌ Authentication required for subjects")
                elif response.status_code == 404:
                    print("❌ Subjects endpoint not found")
                else:
                    print(f"❌ Error: {response.text[:100]}...")

            except Exception as e:
                print(f"❌ Error testing {cert_name}: {e}")
                import traceback
                traceback.print_exc()


async def test_public_endpoints():
    """
    Test public endpoints that don't require authentication.
    """
    print("\n--- Testing Public Endpoints ---")

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:

        # Test public endpoints
        public_endpoints = ["/docs", "/openapi.json"]

        for endpoint in public_endpoints:
            try:
                response = await client.get(endpoint)
                print(f"✅ {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error testing {endpoint}: {e}")


async def setup_test_db():
    """
    Initialize the database for testing.
    """
    try:
        await init_db()
        print("✅ Test database initialized")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


async def main():
    print("UUDEX httpx Test Client")
    print("=" * 50)

    # Initialize database
    print("Initializing test database...")
    db_ready = await setup_test_db()

    if not db_ready:
        print("⚠️  Continuing without database (some tests may fail)")

    # Test public endpoints
    await test_public_endpoints()

    # Test with certificate authentication
    await test_endpoints_with_httpx()

    print("\n✅ Test completed!")


if __name__ == "__main__":
    asyncio.run(main())
