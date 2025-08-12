"""
UUDEX Standalone Client - Certificate Management

This module provides certificate management functionality for the UUDEX CLI
without dependencies on the Reflex web client.
"""

import os
import ssl
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from uudex_api_client import Client
import httpx


class CertificateManager:
    """Manages certificates for UUDEX API authentication"""

    def __init__(self, certs_dir: Optional[str] = None):
        self.certs_dir = certs_dir or os.getenv(
            "CERTS_DIR", os.path.join(os.getcwd(), "certs"))
        self.available_entities: List[str] = []
        self.entity_cert_mapping: Dict[str, str] = {}
        self.ca_cert_path: str = ''

    def get_key_and_cert_path(self, entity_name: str) -> Tuple[str, str]:
        """Get the key and certificate paths for an entity"""
        cert_path = self.entity_cert_mapping.get(entity_name, "")
        key_path = Path(cert_path).parent.joinpath(
            Path(Path(cert_path).stem + ".key"))
        return str(key_path), cert_path

    def get_cert_path(self, entity_name: str) -> str:
        """Get certificate path for an entity"""
        return self.entity_cert_mapping.get(entity_name, "")

    def get_ca_path(self) -> str:
        """Get CA certificate path"""
        return self.ca_cert_path

    def build_client(self,
                     entity_name: str,
                     base_url: str = "https://localhost") -> Client:
        """Build a UUDEX API client for the specified entity"""
        key_file, cert_file = self.get_key_and_cert_path(entity_name)

        httpx_args = {
            'cert': (cert_file, key_file),
            'verify': self.ca_cert_path if self.ca_cert_path else False,
        }

        auth_client = Client(base_url=base_url, httpx_args=httpx_args)
        return auth_client

    def load_entities_from_certs(self) -> None:
        """Load entities by reading certificates from the directory"""
        cert_dir = Path(self.certs_dir)

        if not cert_dir.exists():
            cert_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created certificates directory at {cert_dir}")
            return

        print(f"Loading certificates from: {cert_dir}")

        entities = []
        entity_cert_mapping = {}

        # Find the CA certificate
        for cert_file in cert_dir.glob('*.crt'):
            try:
                if cert_file.name == 'ca.crt':
                    self.ca_cert_path = str(cert_file.resolve())
                    print(f"Found CA certificate: {self.ca_cert_path}")
                    break
            except Exception as e:
                print(f"Error processing certificate {cert_file}: {e}")

        # Process certificate files
        for cert_file in cert_dir.glob('*.crt'):
            try:
                if cert_file.name == 'ca.crt':
                    continue  # Skip CA certificate

                cert_path = str(cert_file.resolve())
                with open(cert_path, 'rb') as f:
                    cert_data = f.read()
                    cert = x509.load_pem_x509_certificate(
                        cert_data, default_backend())

                    # Extract the Common Name from the subject
                    subject = cert.subject
                    common_names = [
                        attr.value for attr in subject
                        if attr.oid == x509.NameOID.COMMON_NAME
                    ]

                    if common_names:
                        common_name = common_names[0]
                        entities.append(common_name)
                        entity_cert_mapping[common_name] = cert_path
                        print(
                            f"Found entity: {common_name} from certificate: {cert_file}"
                        )

            except Exception as e:
                print(f"Error processing certificate {cert_file}: {e}")

        self.available_entities = entities
        self.entity_cert_mapping = entity_cert_mapping

        if not entities:
            print("No valid certificates found in directory")

    def test_client_authentication(self, entity_name: str) -> bool:
        """Test if a client can authenticate with the API"""
        try:
            client = self.build_client(entity_name)
            httpx_client = client.get_httpx_client()

            # Test authentication with /endpoint/me
            response = httpx_client.get("/endpoint/me")

            if response.status_code == 200:
                print(f"✓ Successfully authenticated as {entity_name}")
                return True
            else:
                print(
                    f"✗ Authentication failed for {entity_name}: {response.status_code}"
                )
                return False

        except Exception as e:
            print(f"✗ Authentication error for {entity_name}: {e}")
            return False
