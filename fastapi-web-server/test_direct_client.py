#!/usr/bin/env python3
"""
Direct FastAPI test client for querying subjects.
This bypasses the certificate authentication for testing purposes.
"""

import sys
import asyncio
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from fastapi.testclient import TestClient
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
    # Simulate different certificate subjects based on cert name
    cert_subjects = {
        "alice": "CN=alice,O=Acme Corp,C=US",
        "pnnl": "CN=0a476033-5cc6-4050-a289-ddf11a8fe0d4-pnnl-client,O=PNNL,C=US",
        "acme": "CN=fb9afb6d-566-ACME-Publisher,O=ACME Publisher,C=US"
    }

    subject = cert_subjects.get(cert_name, cert_subjects["alice"])

    return {
        "X-Client-Cert-Subject": subject,
        "X-Client-Cert-Issuer": "CN=LocalCA,O=Test CA,C=US",
        "X-Client-Cert-Serial": "123456789"
    }


def test_subjects_endpoint():
    """
    Test the subjects endpoint using FastAPI TestClient.
    """
    print("Testing UUDEX Subjects Endpoint")
    print("=" * 40)

    # Create test client
    client = TestClient(app)

    # Test different certificates
    test_certs = ["alice", "pnnl", "acme"]

    for cert_name in test_certs:
        print(f"\n--- Testing with {cert_name} certificate ---")

        # Get certificate headers
        headers = simulate_certificate_headers(cert_name)
        print(f"Subject: {headers['X-Client-Cert-Subject']}")

        try:
            # Test basic root endpoint
            response = client.get("/", headers=headers)
            print(f"Root endpoint status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                cert_info = data.get("certificate_info", {})
                print(f"Extracted CN: {cert_info.get('cn', 'Not found')}")

            # Test endpoint/me
            response = client.get("/endpoint/me", headers=headers)
            print(f"Endpoint/me status: {response.status_code}")

            if response.status_code == 200:
                endpoint_data = response.json()
                print(f"✅ Endpoint user: {endpoint_data.get('endpoint_user_name', 'Not found')}")
                print(f"   Endpoint ID: {endpoint_data.get('endpoint_id', 'Not found')}")
                print(f"   Participant ID: {endpoint_data.get('participant_id', 'Not found')}")
            elif response.status_code == 401:
                print("❌ Authentication required - certificate not found in database")
            else:
                print(f"❌ Unexpected response: {response.text[:100]}...")

            # Test subjects endpoint (try both discovery and get_all)
            print("Testing subjects discovery...")
            response = client.get("/subjects/discover", headers=headers)
            print(f"Subjects discover status: {response.status_code}")

            if response.status_code == 200:
                subjects = response.json()
                print(f"✅ Found {len(subjects)} discoverable subjects")
                for i, subject in enumerate(subjects[:3], 1):    # Show first 3
                    subject_name = subject.get('subject_name', 'Unknown') if isinstance(
                        subject, dict) else str(subject)
                    print(f"   {i}. {subject_name}")
                if len(subjects) > 3:
                    print(f"   ... and {len(subjects) - 3} more")
            elif response.status_code == 401:
                print("❌ Authentication required for subjects discovery")
            else:
                print(f"❌ Subjects discovery error: {response.text[:100]}...")

            # Also try get all subjects
            print("Testing get all subjects...")
            response = client.get("/subjects/", headers=headers)
            print(f"Get all subjects status: {response.status_code}")

            if response.status_code == 200:
                subjects = response.json()
                print(f"✅ Found {len(subjects)} total subjects")
                for i, subject in enumerate(subjects[:3], 1):    # Show first 3
                    subject_name = subject.get('subject_name', 'Unknown') if isinstance(
                        subject, dict) else str(subject)
                    print(f"   {i}. {subject_name}")
                if len(subjects) > 3:
                    print(f"   ... and {len(subjects) - 3} more")
            elif response.status_code == 401:
                print("❌ Authentication required for get all subjects")
            elif response.status_code == 404:
                print("❌ Subjects endpoint not found - check routes")
            else:
                print(f"❌ Get all subjects error: {response.text[:100]}...")

        except Exception as e:
            print(f"❌ Error testing {cert_name}: {e}")
            import traceback
            traceback.print_exc()


def test_without_auth():
    """
    Test public endpoints that don't require authentication.
    """
    print("\n--- Testing Public Endpoints ---")

    client = TestClient(app)

    # Test public endpoints
    public_endpoints = ["/docs", "/openapi.json"]

    for endpoint in public_endpoints:
        try:
            response = client.get(endpoint)
            print(f"{endpoint}: {response.status_code}")
        except Exception as e:
            print(f"Error testing {endpoint}: {e}")


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


def main():
    print("UUDEX FastAPI Direct Test Client")
    print("=" * 50)

    # Parse command line arguments for certificate choice
    import argparse
    parser = argparse.ArgumentParser(
        description="Test UUDEX API with simulated certificate authentication")
    parser.add_argument("--cert",
                        "-c",
                        default="alice",
                        choices=["alice", "pnnl", "acme"],
                        help="Certificate to simulate (default: alice)")
    parser.add_argument("--no-db", action="store_true", help="Skip database initialization")
    args = parser.parse_args()

    cert_name = args.cert
    print(f"Using simulated certificate: {cert_name}")

    # Initialize database unless skipped
    if not args.no_db:
        print("\nInitializing test database...")
        db_ready = asyncio.run(setup_test_db())

        if not db_ready:
            print("⚠️  Continuing without database (some tests may fail)")
    else:
        print("⚠️  Skipping database initialization")

    # Test public endpoints
    test_without_auth()

    # Test with certificate authentication
    test_subjects_endpoint()

    # Show next steps
    print("\n" + "=" * 50)
    print("🚀 Next Steps:")
    print("1. Try the full mTLS client: python query_subjects.py --cert alice")
    print(
        "2. Check if endpoints are in database: python -c \"from tests.conftest import *; print('Check DB')\""
    )
    print(
        "3. Ensure Caddy is running: docker-compose -f infrastructure/caddy/docker-compose.yml up -d"
    )
    print("4. Test different certificates: alice, pnnl, acme")

    print("\n✅ Test completed!")


if __name__ == "__main__":
    main()
