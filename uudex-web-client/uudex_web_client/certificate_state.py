from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import os
import threading
from typing import List, Dict, Optional, Any
from pathlib import Path
import ssl

from dotenv import load_dotenv
import httpx
from pydantic import BaseModel
import reflex as rx

from uudex_api_client import Client
from .config import uudex_config


class LocalEntryPoint(BaseModel):
    """Represents a local entry point for the application."""
    certificate_dn: str
    user_name: str
    active_sw: str
    uudex_administrator_sw: str
    participant_administrator_sw: str
    participant_id: int
    participant_uuid: str
    name: str

    def __str__(self):
        return f"{self.name} - {self.description} ({self.url})"

    def __hash__(self):
        return hash((self.certificate_dn, self.user_name, self.participant_id))


class EndPoints:

    def __init__(self):
        self._endpoints: set[LocalEntryPoint] = set()
        self._lock = threading.RLock()

    def add_endpoint(self, endpoint: LocalEntryPoint):
        with self._lock:
            self._endpoints.add(endpoint)

    def get_endpoint_by(self, key: str,
                        key_value: str) -> Optional[LocalEntryPoint]:
        with self._lock:
            for endpoint in self._endpoints:
                if getattr(endpoint, key, None) == key_value:
                    return endpoint
        return None

    def get_by_username(self, username: str) -> Optional[LocalEntryPoint]:
        return self.get_endpoint_by("user_name", username)


# Module-level client cache with TTL (not part of Reflex state)
import time
import os


class ClientCache:

    def __init__(self, ttl_seconds: int = 600):
        self._cache: Dict[str, tuple[Client, float]] = {}
        self._lock = threading.RLock()
        self._ttl = ttl_seconds

    def get(self, entity_name: str) -> Optional[Client]:
        with self._lock:
            entry = self._cache.get(entity_name)
            if entry:
                client, created_at = entry
                if time.time() - created_at < self._ttl:
                    return client
                else:
                    # Expired
                    del self._cache[entity_name]
            return None

    def set(self, entity_name: str, client: Client):
        with self._lock:
            self._cache[entity_name] = (client, time.time())


def _get_client_cache_ttl() -> int:
    try:
        return int(os.environ.get("CLIENT_CACHE_TTL", "600"))
    except Exception:
        return 600


_client_cache = ClientCache(ttl_seconds=_get_client_cache_ttl())

endpoints = EndPoints()


class CertificateState(rx.State):
    """Shared state for certificate management."""

    available_entities: List[str] = []
    entity_cert_mapping: Dict[str, str] = {
    }  # Maps entity names to certificate files
    certs_dir: str = uudex_config.CERTS_DIR  # Get directory from env var or use default

    ca_cert_path: str = ''

    def _get_key_and_cert_path(self, entity_name: str) -> tuple[str, str]:
        cert_path = self.entity_cert_mapping.get(entity_name, "")
        key_path = Path(cert_path).parent.joinpath(
            Path(Path(cert_path).stem + ".key"))
        return key_path.as_posix(), cert_path

    @rx.event
    def get_key_and_cert_path(self, entity_name: str) -> tuple[str, str]:
        return self._get_key_and_cert_path(entity_name)

    @rx.event
    def get_cert_path(self, entity_name: str) -> str:
        """Backend event to safely get certificate path for an entity."""
        # This runs on the backend so we can use regular Python dictionary operations
        return self.entity_cert_mapping.get(entity_name, "")

    @rx.event
    def get_ca_path(self) -> str:
        return self.ca_cert_path
        key_file, cert_file = self._get_key_and_cert_path(entity_name)

    def get_client(self, entity_name: str) -> Client:
        """
        Return a cached or new configured Client for the given entity name.
        """
        client = _client_cache.get(entity_name)
        if client is not None:
            return client
        key_file, cert_file = self._get_key_and_cert_path(entity_name)
        httpx_args = {
            'cert': (cert_file, key_file),
        }
        client = Client(base_url="https://localhost",
                        verify_ssl=self.ca_cert_path,
                        httpx_args=httpx_args)
        _client_cache.set(entity_name, client)
        return client

    async def load_entities_from_certs(self):
        """Load entities by reading certificates from a directory."""
        try:
            # Use the cert directory from environment variable
            cert_dir = Path(self.certs_dir)

            print(f"Loading certificates from: {cert_dir}")

            if not cert_dir.exists():
                cert_dir.mkdir(parents=True, exist_ok=True)
                print(f"Created certificates directory at {cert_dir}.")
                # Add some sample entities for demonstration if no certs are found
                self.available_entities = [
                    "Entity A", "Entity B", "Entity C", "Entity D"
                ]
                return

            entities = []
            entity_cert_mapping = {}

            # Find the CA certificate
            for cert_file in cert_dir.glob('*.crt'):
                try:
                    if cert_file.as_posix().endswith('ca.crt'):
                        self.ca_cert_path = cert_file.resolve().as_posix()
                        break
                except Exception as e:
                    print(f"Error processing certificate {cert_file}: {e}")

            # Find the certificate and check that we can call /me on the backend.
            for cert_file in cert_dir.glob('*.crt'):
                try:
                    if cert_file.as_posix().endswith('ca.crt'):
                        continue  # Skip CA certificate
                    cert_path = cert_file.resolve().as_posix()
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
                            entity_cert_mapping[common_name] = str(cert_file)
                            print(
                                f"Found entity: {common_name} from certificate: {cert_file}"
                            )

                            auth_client = self.build_client(common_name)
                            httpx_client = auth_client.get_httpx_client()
                            endpoint = httpx_client.get(
                                "/endpoint/me")  # Test the client

                            if endpoint.status_code == 200:
                                print(
                                    f"Successfully authenticated as {common_name}"
                                )

                                data = endpoint.json()

                                ep = LocalEntryPoint(
                                    certificate_dn=data.get("certificate_dn"),
                                    user_name=data.get("endpoint_user_name"),
                                    active_sw=data.get("active_sw", "N"),
                                    uudex_administrator_sw=data.get(
                                        "uudex_administrator_sw", "N"),
                                    participant_administrator_sw=data.get(
                                        "participant_administrator_sw", "N"),
                                    participant_id=data.get(
                                        "participant_id", 0),
                                    participant_uuid=data.get(
                                        "participant_uuid", ""),
                                    name=common_name)
                                endpoints.add_endpoint(ep)
                                # ep = LocalEntryPoint(certificate_dn=data.get("certificate_dn"),

                                # cn: str
                                # user_name: str
                                # active_sw: str
                                # uudex_administrator_sw: str
                                # participant_administrator_sw: str
                                # participant_id: int
                                # participant_uuid: str
                                # name: str

                            else:
                                print(
                                    f"Failed to authenticate {common_name}: {endpoint.status_code} {endpoint.text}"
                                )
                except Exception as e:
                    print(f"Error processing certificate {cert_file}: {e}")

            if entities:
                self.available_entities = entities
                self.entity_cert_mapping = entity_cert_mapping
            else:
                # If no valid certificates were found, add sample entities
                self.available_entities = [
                    "Entity A", "Entity B", "Entity C", "Entity D"
                ]

        except Exception as e:
            print(f"Error loading certificates: {str(e)}")
            # Add some sample entities for demonstration
            self.available_entities = [
                "Entity A", "Entity B", "Entity C", "Entity D"
            ]
