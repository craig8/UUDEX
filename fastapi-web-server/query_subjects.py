#!/usr/bin/env python3
"""
UUDEX mTLS API Query Client

This script provides a comprehensive client for querying UUDEX API endpoints using
certificate-based mutual TLS authentication. It supports all major UUDEX endpoints:
- subjects: Data subjects/topics
- datasets: Available datasets
- participants: System participants/organizations
- endpoints: Client endpoints and certificates
- subscriptions: Data subscriptions

Usage examples:
    python query_subjects.py alice subjects          # Query subjects with alice cert
    python query_subjects.py pnnl datasets           # Query datasets with pnnl cert
    python query_subjects.py acme participants       # Query participants with acme cert
    python query_subjects.py --cert alice endpoints  # Query endpoints with alice cert
    python query_subjects.py --test-only alice       # Test connection only
"""

import sys
import ssl
import json
import asyncio
import urllib3
from pathlib import Path

try:
    import httpx
except ImportError:
    print("❌ Error: 'httpx' library is required but not installed.")
    print("Please install it with: pip install httpx")
    sys.exit(1)

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def setup_client_with_certificates(cert_name="alice"):
    """
    Set up certificate paths for mTLS authentication.

    Args:
        cert_name: Name of certificate to use (alice, pnnl, or acme)

    Returns:
        dict: Certificate configuration with file paths
    """
    # Certificate paths - look in the infrastructure/caddy/certs directory
    cert_dir = Path("./infrastructure/caddy/certs")

    # Map cert names to actual file names
    cert_mappings = {
        "alice": "3fa9be8b-a0f9-40a5-ab3d-51d580d4797e_alice",
        "pnnl": "0a476033-5cc6-4050-a289-ddf11a8fe0d4-pnnl-client",
        "acme": "fb9afb6d-566-ACME-Publisher"
    }

    if cert_name not in cert_mappings:
        print(f"❌ Unknown certificate name: {cert_name}")
        print(f"Available certificates: {list(cert_mappings.keys())}")
        return None

    # Use specified certificate for authentication
    cert_base_name = cert_mappings[cert_name]
    client_cert = cert_dir / f"{cert_base_name}.crt"
    client_key = cert_dir / f"{cert_base_name}.key"
    ca_cert = cert_dir / "ca.crt"

    print(f"Looking for certificates in: {cert_dir.absolute()}")

    # Verify certificate files exist
    missing_files = []
    for cert_file, name in [(client_cert, "client certificate"), (client_key, "private key"),
                            (ca_cert, "CA certificate")]:
        if not cert_file.exists():
            missing_files.append(f"{name}: {cert_file}")

    if missing_files:
        print("❌ Missing certificate files:")
        for missing in missing_files:
            print(f"   {missing}")
        print("\nPlease generate certificates first using:")
        print("   cd infrastructure/caddy && ./generate-certs.sh")
        return None

    print(f"✅ Using client certificate: {client_cert.name}")
    print(f"✅ Using private key: {client_key.name}")
    print(f"✅ Using CA certificate: {ca_cert.name}")

    return {
        "cert_file": str(client_cert),
        "key_file": str(client_key),
        "ca_cert": str(ca_cert),
        "cert_name": cert_name
    }


async def query_api_endpoint(cert_name="alice",
                             base_url="https://localhost",
                             endpoint_type="subjects",
                             **query_params):
    """
    Query any UUDEX API endpoint using mTLS authentication.

    Args:
        cert_name: Certificate to use for authentication
        base_url: Base URL of the UUDEX server
        endpoint_type: Type of endpoint to query (subjects, participants, subscriptions)
        **query_params: Additional query parameters to pass to the API

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Set up certificate configuration
        config = setup_client_with_certificates(cert_name)
        if not config:
            return False

        # Map endpoint types to their API paths and display names
        endpoint_config = {
            "subjects": {
                "path":
                "/subjects/",
                "name":
                "Subjects",
                "item_name_key":
                "subject_name",
                "item_id_key":
                "subject_id",
                "supported_params":
                ["limit", "offset", "subject_name", "participant_id", "subscription_type"]
            },
            "participants": {
                "path":
                "/participants/",
                "name":
                "Participants",
                "item_name_key":
                "participant_long_name",
                "item_id_key":
                "participant_id",
                "supported_params":
                ["limit", "offset", "participant_name", "active_only", "organization"]
            },
            "subscriptions": {
                "path":
                "/subscriptions/",
                "name":
                "Subscriptions",
                "item_name_key":
                "subscription_name",
                "item_id_key":
                "subscription_id",
                "supported_params":
                ["limit", "offset", "subscription_name", "state", "owner_endpoint_id"]
            }
        }

        if endpoint_type not in endpoint_config:
            print(f"❌ Unknown endpoint type: {endpoint_type}")
            print(f"Available endpoints: {list(endpoint_config.keys())}")
            return False

        config_info = endpoint_config[endpoint_type]

        # Filter query parameters to only supported ones
        filtered_params = {}
        if query_params:
            supported_params = config_info.get("supported_params", [])
            for param, value in query_params.items():
                if param in supported_params and value is not None:
                    filtered_params[param] = value

            if filtered_params:
                print(f"📋 Query parameters: {filtered_params}")

        print(f"\n🔐 Connecting to UUDEX server with {cert_name} certificate...")
        print(f"Server URL: {base_url}")
        print(f"Querying: {config_info['name']}")

        # Create httpx client with mTLS configuration
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.load_verify_locations(config["ca_cert"])
        ssl_context.load_cert_chain(config["cert_file"], config["key_file"])
        ssl_context.check_hostname = False    # For self-signed certificates

        timeout = httpx.Timeout(10.0)

        async with httpx.AsyncClient(verify=ssl_context, timeout=timeout) as client:

            # Test basic connection first
            print("\n--- Testing Connection ---")
            try:
                response = await client.get(f"{base_url}/")
                print(f"✅ Root endpoint: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    cert_info = data.get("certificate_info", {})
                    print(f"   Detected CN: {cert_info.get('cn', 'Not found')}")
                else:
                    print(f"   Response: {response.text[:100]}...")

            except httpx.SSLError as e:
                print(f"❌ SSL Error: {e}")
                print("   This might indicate certificate validation issues")
                return False
            except httpx.ConnectError as e:
                print(f"❌ Connection Error: {e}")
                print("   Is the UUDEX server running? Try: docker-compose up -d")
                return False
            except Exception as e:
                print(f"❌ Connection test failed: {e}")
                return False

            # Test authentication
            print("\n--- Testing Authentication ---")
            try:
                response = await client.get(f"{base_url}/endpoint/me")
                print(f"Authentication endpoint: {response.status_code}")

                if response.status_code == 200:
                    endpoint_data = response.json()
                    print(
                        f"✅ Authenticated as: {endpoint_data.get('endpoint_user_name', 'Unknown')}"
                    )
                    print(f"   Endpoint ID: {endpoint_data.get('endpoint_id', 'Unknown')}")
                    print(f"   Participant ID: {endpoint_data.get('participant_id', 'Unknown')}")
                elif response.status_code == 401:
                    print("❌ Authentication failed - certificate not in database")
                    print("   The certificate DN may not be registered in the endpoints table")
                    return False
                else:
                    print(f"❌ Unexpected response: {response.text[:100]}...")
                    return False

            except Exception as e:
                print(f"❌ Authentication test failed: {e}")
                return False

            # Query the requested endpoint
            print(f"\n--- Querying {config_info['name']} ---")
            try:
                # Build URL with query parameters
                url = f"{base_url}{config_info['path']}"
                if filtered_params:
                    # Convert parameters to query string
                    query_string = "&".join([f"{k}={v}" for k, v in filtered_params.items()])
                    url = f"{url}?{query_string}"
                    print(f"Request URL: {url}")

                response = await client.get(url)
                print(f"{config_info['name']} endpoint: {response.status_code}")

                if response.status_code == 200:
                    items = response.json()
                    print(f"✅ Found {len(items)} {config_info['name'].lower()}:")

                    # Display items in a nice format
                    for i, item in enumerate(items[:15], 1):    # Show first 15
                        if isinstance(item, dict):
                            name = item.get(config_info['item_name_key'], 'Unknown')
                            item_id = item.get(config_info['item_id_key'], 'N/A')
                            description = item.get('description', '')

                            print(f"   {i:2d}. {name} (ID: {item_id})")

                            # Show additional relevant fields based on endpoint type
                            if endpoint_type == "participants":
                                short_name = item.get('participant_short_name', '')
                                org = item.get('organization', '')
                                active = item.get('active_sw', 'N') == 'Y'
                                status = "Active" if active else "Inactive"
                                print(f"       Short Name: {short_name}")
                                print(f"       Status: {status}")
                                if org:
                                    print(f"       Organization: {org}")
                            elif endpoint_type == "subscriptions":
                                state = item.get('subscription_state', '')
                                owner_id = item.get('owner_endpoint_id', '')
                                if state:
                                    print(f"       State: {state}")
                                if owner_id:
                                    print(f"       Owner Endpoint ID: {owner_id}")

                            if description:
                                print(
                                    f"       Description: {description[:80]}{'...' if len(description) > 80 else ''}"
                                )
                        else:
                            print(f"   {i:2d}. {item}")

                    if len(items) > 15:
                        print(f"   ... and {len(items) - 15} more {config_info['name'].lower()}")

                    # Save items to file for reference
                    output_file = f"{endpoint_type}_{cert_name}.json"
                    with open(output_file, 'w') as f:
                        json.dump(items, f, indent=2, default=str)
                    print(f"\n💾 {config_info['name']} saved to: {output_file}")

                    return True

                elif response.status_code == 401:
                    print(f"❌ Authentication required for {config_info['name'].lower()}")
                    return False
                elif response.status_code == 403:
                    print(f"❌ Access forbidden for {config_info['name'].lower()}")
                    print("   Your certificate may not have permission to access this endpoint")
                    return False
                elif response.status_code == 404:
                    print(f"❌ {config_info['name']} endpoint not found")
                    return False
                else:
                    print(f"❌ Error: {response.text[:100]}...")
                    return False

            except Exception as e:
                print(f"❌ {config_info['name']} query failed: {e}")
                return False

    except Exception as e:
        print(f"❌ Failed to query {endpoint_type}: {e}")
        import traceback
        traceback.print_exc()
        return False


async def list_available_endpoints(cert_name="alice", base_url="https://localhost"):
    """
    List all available API endpoints and test basic connectivity.

    Args:
        cert_name: Certificate to use for authentication
        base_url: Base URL of the UUDEX server
    """
    endpoints = ["subjects", "participants", "subscriptions"]

    print(f"\n📋 Testing all UUDEX API endpoints with {cert_name} certificate...")
    print(f"Server: {base_url}")
    print("-" * 60)

    results = {}

    for endpoint in endpoints:
        try:
            config = setup_client_with_certificates(cert_name)
            if not config:
                results[endpoint] = "❌ Certificate setup failed"
                continue

            ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ssl_context.load_verify_locations(config["ca_cert"])
            ssl_context.load_cert_chain(config["cert_file"], config["key_file"])
            ssl_context.check_hostname = False

            timeout = httpx.Timeout(5.0)

            async with httpx.AsyncClient(verify=ssl_context, timeout=timeout) as client:
                response = await client.get(f"{base_url}/{endpoint}/")

                if response.status_code == 200:
                    data = response.json()
                    count = len(data) if isinstance(data, list) else "N/A"
                    results[endpoint] = f"✅ {response.status_code} ({count} items)"
                elif response.status_code == 401:
                    results[endpoint] = "🔒 401 (Authentication required)"
                elif response.status_code == 403:
                    results[endpoint] = "🚫 403 (Access forbidden)"
                elif response.status_code == 404:
                    results[endpoint] = "❓ 404 (Not found)"
                else:
                    results[endpoint] = f"⚠️ {response.status_code}"

        except httpx.ConnectError:
            results[endpoint] = "🔌 Connection failed"
        except httpx.SSLError:
            results[endpoint] = "🛡️ SSL/Certificate error"
        except Exception as e:
            results[endpoint] = f"❌ Error: {str(e)[:30]}..."

    # Display results
    print(f"{'Endpoint':<15} {'Status':<30}")
    print("-" * 45)
    for endpoint, status in results.items():
        print(f"{endpoint:<15} {status}")

    print(f"\n💡 To query a specific endpoint:")
    print(f"   python query_subjects.py {cert_name} <endpoint_name>")
    print(f"   Available endpoints: {', '.join(endpoints)}")


async def test_connection(cert_name="alice", base_url="https://localhost"):
    """
    Test basic connection to the server.

    Args:
        cert_name: Certificate to use for testing
        base_url: Base URL of the UUDEX server
    """
    try:
        config = setup_client_with_certificates(cert_name)
        if not config:
            return False

        print(f"\n🔧 Testing connection with {cert_name} certificate...")

        # Try httpx connection
        try:
            ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ssl_context.load_verify_locations(config["ca_cert"])
            ssl_context.load_cert_chain(config["cert_file"], config["key_file"])
            ssl_context.check_hostname = False    # For self-signed certificates

            timeout = httpx.Timeout(5.0)

            async with httpx.AsyncClient(verify=ssl_context, timeout=timeout) as client:
                response = await client.get(f"{base_url}/")
                print(f"✅ HTTP connection successful: {response.status_code}")
                return response.status_code < 500    # Accept 2xx, 3xx, 4xx but not 5xx

        except Exception as e:
            print(f"❌ HTTP connection failed: {e}")
            return False

    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


async def main():
    """Main async function to run the mTLS client."""
    print("UUDEX mTLS API Query Client")
    print("=" * 40)

    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(
        description="Query UUDEX API endpoints with mTLS certificate authentication",
        epilog="""
Examples:
  python query_subjects.py subjects                                    # Query subjects with alice certificate (default)
  python query_subjects.py participants --cert pnnl                   # Query participants with pnnl certificate
  python query_subjects.py subscriptions --cert acme                  # Query subscriptions with acme certificate
  python query_subjects.py subjects --limit 5 --subject-name test     # Query subjects with filtering
  python query_subjects.py participants --active-only                 # Show only active participants
  python query_subjects.py list                                       # List all endpoints and their status
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # Main endpoint argument
    parser.add_argument("endpoint",
                        choices=["subjects", "participants", "subscriptions", "list"],
                        help="API endpoint to query")

    # Certificate and server options
    parser.add_argument("--cert",
                        "-c",
                        choices=["alice", "pnnl", "acme"],
                        default="alice",
                        help="Certificate to use for authentication (default: alice)")
    parser.add_argument("--url",
                        "-u",
                        default="https://localhost",
                        help="UUDEX server URL (default: https://localhost)")
    parser.add_argument("--all-certs",
                        action="store_true",
                        help="Test all certificates with the specified endpoint")

    # Common query parameters
    parser.add_argument("--limit", type=int, help="Maximum number of results to return")
    parser.add_argument("--offset", type=int, help="Number of results to skip (for pagination)")

    # Subject-specific parameters
    parser.add_argument("--subject-name", help="Filter subjects by name")
    parser.add_argument("--participant-id", help="Filter subjects by participant ID")
    parser.add_argument("--subscription-type", help="Filter subjects by subscription type")

    # Participant-specific parameters
    parser.add_argument("--participant-name", help="Filter participants by name")
    parser.add_argument("--active-only", action="store_true", help="Show only active participants")
    parser.add_argument("--organization", help="Filter participants by organization")

    # Subscription-specific parameters
    parser.add_argument("--subscription-name", help="Filter subscriptions by name")
    parser.add_argument("--state", help="Filter subscriptions by state")
    parser.add_argument("--owner-endpoint-id", help="Filter subscriptions by owner endpoint ID")

    # Legacy options for backward compatibility
    parser.add_argument("--test-only",
                        "-t",
                        action="store_true",
                        help="Only test connection, don't query API")

    args = parser.parse_args()

    print(f"🔑 Certificate: {args.cert}")
    print(f"🌐 Server URL: {args.url}")

    # Handle special endpoints
    if args.endpoint == "list":
        print(f"📋 Mode: List all endpoints")
        await list_available_endpoints(args.cert, args.url)
        print("\n🏁 Done.")
        return

    if args.test_only:
        print(f"🔧 Mode: Connection test only")
        # Test connection only
        if await test_connection(args.cert, args.url):
            print("\n✅ Connection test passed!")
        else:
            print("\n❌ Connection test failed!")
            print_troubleshooting_tips()
        print("\n🏁 Done.")
        return

    # Build query parameters from arguments
    query_params = {}
    if args.limit is not None:
        query_params["limit"] = args.limit
    if args.offset is not None:
        query_params["offset"] = args.offset

    # Subject parameters
    if args.subject_name:
        query_params["subject_name"] = args.subject_name
    if args.participant_id:
        query_params["participant_id"] = args.participant_id
    if args.subscription_type:
        query_params["subscription_type"] = args.subscription_type

    # Participant parameters
    if args.participant_name:
        query_params["participant_name"] = args.participant_name
    if args.active_only:
        query_params["active_only"] = "true"
    if args.organization:
        query_params["organization"] = args.organization

    # Subscription parameters
    if args.subscription_name:
        query_params["subscription_name"] = args.subscription_name
    if args.state:
        query_params["state"] = args.state
    if args.owner_endpoint_id:
        query_params["owner_endpoint_id"] = args.owner_endpoint_id

    print(f"📊 Endpoint: {args.endpoint}")
    if query_params:
        print(f"🔍 Query parameters: {query_params}")

    if args.all_certs:
        # Test all certificates
        certificates = ["alice", "pnnl", "acme"]
        for cert in certificates:
            print(f"\n{'='*60}")
            print(f"Testing with {cert} certificate")
            print(f"{'='*60}")
            success = await query_api_endpoint(cert, args.url, args.endpoint, **query_params)
            if not success:
                print(f"❌ Failed with {cert} certificate")
    else:
        # Test single certificate
        success = await query_api_endpoint(args.cert, args.url, args.endpoint, **query_params)
        if success:
            print(f"\n✅ Successfully queried {args.endpoint} with {args.cert} certificate")
        else:
            print(f"\n❌ Failed to query {args.endpoint} with {args.cert} certificate")

    print("\n🏁 Done.")


def print_troubleshooting_tips():
    """Print helpful troubleshooting tips for common issues."""
    print("\n🔧 Troubleshooting Tips:")
    print("1. ✅ UUDEX server is running (docker-compose up -d)")
    print("2. ✅ Certificate files are present in infrastructure/caddy/certs/")
    print("3. ✅ Caddy is properly configured and running")
    print("4. ✅ Database contains endpoint data for the certificate")
    print("5. ✅ Server URL is correct")
    print("6. ✅ Network connectivity to the server")
    print("\nTo generate missing certificates:")
    print("   cd infrastructure/caddy && ./generate-certs.sh")
    print("\nTo check server status:")
    print("   docker-compose ps")
    print("   docker-compose logs caddy")


if __name__ == "__main__":
    asyncio.run(main())
