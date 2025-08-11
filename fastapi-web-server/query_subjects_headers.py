#!/usr/bin/env python3
"""
Simple test client that simulates Caddy's certificate header forwarding.
This script sends HTTP requests with certificate information in headers,
simulating what Caddy would do when forwarding client certificate info.
"""

import requests
import urllib3
from pathlib import Path
import ssl
import OpenSSL.crypto
import sys

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def read_certificate_info(cert_path):
    """
    Read certificate information from a .crt file.
    Returns the subject DN that would be sent by Caddy.
    """
    try:
        with open(cert_path, 'rb') as cert_file:
            cert_data = cert_file.read()

        # Parse the certificate
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)

        # Get subject components
        subject = cert.get_subject()
        subject_dn = ", ".join(
            [f"{name.decode()}={value.decode()}" for name, value in subject.get_components()])

        # Get issuer components
        issuer = cert.get_issuer()
        issuer_dn = ", ".join(
            [f"{name.decode()}={value.decode()}" for name, value in issuer.get_components()])

        # Get serial number
        serial = str(cert.get_serial_number())

        return {'subject': subject_dn, 'issuer': issuer_dn, 'serial': serial}

    except Exception as e:
        print(f"Error reading certificate {cert_path}: {e}")
        return None


def test_with_certificate_headers(cert_name="alice"):
    """
    Test the UUDEX server by sending requests with certificate headers,
    simulating what Caddy would send.
    """
    # Certificate paths
    cert_dir = Path(__file__).parent / "infrastructure" / "caddy" / "certs"

    if cert_name == "alice":
        cert_file = cert_dir / "3fa9be8b-a0f9-40a5-ab3d-51d580d4797e_alice.crt"
    elif cert_name == "pnnl":
        cert_file = cert_dir / "0a476033-5cc6-4050-a289-ddf11a8fe0d4-pnnl-client.crt"
    elif cert_name == "acme":
        cert_file = cert_dir / "fb9afb6d-566-ACME-Publisher.crt"
    else:
        print(f"Unknown certificate name: {cert_name}")
        return

    if not cert_file.exists():
        print(f"Certificate file not found: {cert_file}")
        return

    # Read certificate information
    cert_info = read_certificate_info(cert_file)
    if not cert_info:
        return

    print(f"Using certificate: {cert_file.name}")
    print(f"Subject DN: {cert_info['subject']}")
    print(f"Issuer DN: {cert_info['issuer']}")
    print(f"Serial: {cert_info['serial']}")
    print()

    # Set up headers that Caddy would send
    headers = {
        'X-Client-Cert-Subject': cert_info['subject'],
        'X-Client-Cert-Issuer': cert_info['issuer'],
        'X-Client-Cert-Serial': cert_info['serial'],
        'Content-Type': 'application/json'
    }

    # Server URL (assuming local development)
    base_url = "http://localhost:8000"    # Adjust port as needed

    try:
        # Test basic connection
        print("Testing basic connection...")
        response = requests.get(f"{base_url}/", headers=headers, verify=False, timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Basic connection successful")
            try:
                data = response.json()
                print(f"Response: {data}")
            except:
                print(f"Response text: {response.text[:200]}...")
        else:
            print(f"❌ Basic connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return

        print()

        # Test endpoint authentication
        print("Testing /endpoint/me endpoint...")
        response = requests.get(f"{base_url}/endpoint/me",
                                headers=headers,
                                verify=False,
                                timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Endpoint authentication successful")
            try:
                endpoint_data = response.json()
                print(f"Endpoint data: {endpoint_data}")
            except:
                print(f"Response text: {response.text[:200]}...")
        else:
            print(f"❌ Endpoint authentication failed: {response.status_code}")
            print(f"Response: {response.text}")

        print()

        # Test subjects endpoint
        print("Testing /subjects endpoint...")
        response = requests.get(f"{base_url}/subjects/", headers=headers, verify=False, timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Subjects query successful")
            try:
                subjects_data = response.json()
                print(f"Found {len(subjects_data)} subjects:")
                for i, subject in enumerate(subjects_data, 1):
                    print(f"  {i}. {subject}")
            except:
                print(f"Response text: {response.text[:200]}...")
        else:
            print(f"❌ Subjects query failed: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Is the UUDEX server running?")
        print(f"Trying to connect to: {base_url}")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def main():
    print("UUDEX Certificate Header Test Client")
    print("=" * 50)

    # Test with different certificates
    certificates = ["alice", "pnnl", "acme"]

    if len(sys.argv) > 1:
        cert_name = sys.argv[1]
        if cert_name not in certificates:
            print(f"Available certificates: {', '.join(certificates)}")
            sys.exit(1)
        test_with_certificate_headers(cert_name)
    else:
        # Test with Alice certificate by default
        print("Testing with Alice certificate (default)")
        print("Usage: python query_subjects_headers.py [alice|pnnl|acme]")
        print()
        test_with_certificate_headers("alice")


if __name__ == "__main__":
    main()
