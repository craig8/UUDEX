import os
import threading
from pathlib import Path
from typing import Dict, List, Optional

import reflex as rx
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from pydantic import BaseModel
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

    def get_endpoint_by(self, key: str, key_value: str) -> Optional[LocalEntryPoint]:
        with self._lock:
            for endpoint in self._endpoints:
                if getattr(endpoint, key, None) == key_value:
                    return endpoint
        return None

    def get_by_username(self, username: str) -> Optional[LocalEntryPoint]:
        return self.get_endpoint_by("user_name", username)


# Module-level client cache with TTL (not part of Reflex state)
import os
import time


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
    entity_cert_mapping: Dict[str, str] = {}  # Maps entity names to certificate files
    admin_display_names: List[str] = []  # Display names (endpoint_user_name) for admin dropdown
    display_name_to_cert_name: Dict[str, str] = {}  # Maps display names back to cert names
    certs_dir: str = uudex_config.CERTS_DIR  # Get directory from env var or use default

    ca_cert_path: str = ""

    def _get_key_and_cert_path(self, entity_name: str) -> tuple[str, str]:
        cert_path = self.entity_cert_mapping.get(entity_name, "")
        key_path = Path(cert_path).parent.joinpath(Path(Path(cert_path).stem + ".key"))
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

    @rx.event  
    def get_cert_name_from_display(self, display_name: str) -> str:
        """Convert display name back to certificate name for authentication."""
        return self.display_name_to_cert_name.get(display_name, display_name)

    def get_client(self, entity_name: str) -> Client:
        """
        Return a cached or new configured Client for the given entity name.
        """
        client = _client_cache.get(entity_name)
        if client is not None:
            return client
        key_file, cert_file = self._get_key_and_cert_path(entity_name)
        httpx_args = {
            "cert": (cert_file, key_file),
        }
        client = Client(
            base_url="https://localhost",
            verify_ssl=self.ca_cert_path,
            httpx_args=httpx_args,
        )
        _client_cache.set(entity_name, client)
        return client

    async def load_entities_from_certs(self):
        """Load entities by reading certificates from a directory."""
        import time
        print(f"[DEBUG] load_entities_from_certs called at {time.time()}")
        
        # Initialize admin tracking lists at the method level
        admin_entities = []
        admin_display_names = []
        admin_cert_mapping = {}
        
        try:
            # Use the cert directory from environment variable
            cert_dir = Path(self.certs_dir)

            print(f"[DEBUG] Loading certificates from: {cert_dir}")

            if not cert_dir.exists():
                cert_dir.mkdir(parents=True, exist_ok=True)
                print(f"Created certificates directory at {cert_dir}.")

            # Check if directory is empty or has no cert files
            cert_files = list(cert_dir.glob('*.crt')) + list(cert_dir.glob('*.pem'))
            if not cert_files:
                print("[DEBUG] No certificate files found, using sample entities")
                # Add some sample entities for demonstration if no certs are found
                self.available_entities = [
                    "Entity A",
                    "Entity B",
                    "Entity C",
                    "Entity D",
                ]
                # Create sample entity mapping for testing
                self.entity_cert_mapping = {
                    "Entity A": "",
                    "Entity B": "",
                    "Entity C": "",
                    "Entity D": "",
                }
                print(f"[DEBUG] Set available_entities to: {self.available_entities}")
                print(f"[DEBUG] Set entity_cert_mapping to: {self.entity_cert_mapping}")
                return

            entities = []
            entity_cert_mapping = {}

            # Find the CA certificate
            for cert_file in cert_dir.glob("*.crt"):
                try:
                    if cert_file.as_posix().endswith("ca.crt"):
                        self.ca_cert_path = cert_file.resolve().as_posix()
                        break
                except Exception as e:
                    print(f"Error processing certificate {cert_file}: {e}")

            # Find the certificate and check that we can call /me on the backend.
            for cert_file in cert_dir.glob("*.crt"):
                try:
                    if cert_file.as_posix().endswith("ca.crt"):
                        continue  # Skip CA certificate
                    cert_path = cert_file.resolve().as_posix()
                    with open(cert_path, "rb") as f:
                        cert_data = f.read()
                        cert = x509.load_pem_x509_certificate(
                            cert_data, default_backend()
                        )

                        # Extract the Common Name from the subject
                        subject = cert.subject
                        common_names = [
                            attr.value
                            for attr in subject
                            if attr.oid == x509.NameOID.COMMON_NAME
                        ]

                        if common_names:
                            common_name = common_names[0]
                            cert_file_path = str(cert_file)
                            print(
                                f"Found entity: {common_name} from certificate: {cert_file}"
                            )

                            # Add entity to the list
                            entities.append(common_name)
                            entity_cert_mapping[common_name] = cert_file_path

                            # Try to verify this entity exists on the server and has admin privileges
                            try:
                                auth_client = self.get_client(common_name)
                                httpx_client = auth_client.get_httpx_client()
                                print(f"[DEBUG] Testing {common_name} - calling /endpoint/me")
                                endpoint = httpx_client.get(
                                    "/endpoint/me", timeout=5.0
                                )
                                print(f"[DEBUG] Response for {common_name}: {endpoint.status_code}")

                                if endpoint.status_code == 200:
                                    data = endpoint.json()
                                    print(f"[DEBUG] {common_name} data: {data}")

                                    # Use endpoint_user_name for display, fall back to common_name
                                    display_name = data.get("endpoint_user_name", common_name)
                                    if not display_name or display_name.strip() == "":
                                        display_name = common_name

                                    # Check if this entity is an admin
                                    is_uudex_admin = data.get("uudex_administrator_sw", "N").upper() == "Y"
                                    is_participant_admin = data.get("participant_administrator_sw", "N").upper() == "Y"
                                    print(f"[DEBUG] {display_name}: uudex_admin={is_uudex_admin}, participant_admin={is_participant_admin}")

                                    if is_uudex_admin or is_participant_admin:
                                        # Add to admin entities with server data
                                        admin_entry = {
                                            "name": common_name,
                                            "display_name": display_name,
                                            "endpoint_user_name": data.get("endpoint_user_name", common_name),
                                            "is_uudex_admin": is_uudex_admin,
                                            "is_participant_admin": is_participant_admin,
                                            "is_active": data.get("active_sw", "N") == "Y",
                                            "participant_id": data.get("participant_id", 0)
                                        }
                                        admin_entities.append(admin_entry)
                                        # Also track for easier access
                                        admin_display_names.append(display_name)
                                        admin_cert_mapping[common_name] = entity_cert_mapping.get(common_name, cert_file_path)
                                        
                                        admin_type = []
                                        if is_uudex_admin:
                                            admin_type.append("UUDEX Admin")
                                        if is_participant_admin:
                                            admin_type.append("Participant Admin")
                                        print(f"[DEBUG] Admin found: {display_name} ({', '.join(admin_type)}) - total admins: {len(admin_entities)}")
                                    else:
                                        print(f"Entity exists but not admin: {display_name}")
                                else:
                                    print(f"Failed to verify entity {common_name}: {endpoint.status_code}")

                                # Create LocalEntryPoint with server data
                                ep = LocalEntryPoint(
                                    certificate_dn=data.get("certificate_dn", str(cert.subject)),
                                    user_name=data.get("endpoint_user_name", common_name),
                                    active_sw=data.get("active_sw", "N"),
                                    uudex_administrator_sw=data.get("uudex_administrator_sw", "N"),
                                    participant_administrator_sw=data.get("participant_administrator_sw", "N"),
                                    participant_id=data.get("participant_id", 0),
                                    participant_uuid=data.get("participant_uuid", ""),
                                    name=display_name,
                                )
                                endpoints.add_endpoint(ep)
                            except Exception as api_error:
                                print(f"[DEBUG] Could not verify entity {common_name} on server: {api_error}")
                                # Don't add to admin list if we can't verify on server
                except Exception as e:
                    print(f"Error processing certificate {cert_file}: {e}")

            # Only show admin entities in the dropdown
            print(f"[DEBUG] Final admin_entities count: {len(admin_entities)}")
            print(f"[DEBUG] Admin display names collected: {admin_display_names}")
            
            if admin_entities:
                # Sort admin entities by endpoint_user_name
                admin_entities.sort(key=lambda x: x["endpoint_user_name"].lower())
                
                # Re-extract after sorting
                sorted_admin_names = [admin["name"] for admin in admin_entities]
                sorted_display_names = [admin["display_name"] for admin in admin_entities]
                display_name_mapping = {admin["display_name"]: admin["name"] for admin in admin_entities}

                print(f"[DEBUG] Found {len(admin_entities)} admin entities out of {len(entities)} total entities")
                
                self.available_entities = sorted_admin_names
                self.entity_cert_mapping = admin_cert_mapping
                self.admin_display_names = sorted_display_names
                self.display_name_to_cert_name = display_name_mapping
                print(f"[DEBUG] Set admin_display_names to: {sorted_display_names}")
            elif admin_display_names:
                # If we tracked some admins but admin_entities is somehow empty, use the tracked ones
                print(f"[DEBUG] Using tracked admin_display_names: {admin_display_names}")
                self.available_entities = list(admin_cert_mapping.keys())
                self.entity_cert_mapping = admin_cert_mapping
                self.admin_display_names = admin_display_names
                self.display_name_to_cert_name = {name: name for name in admin_display_names}
            elif entities:
                # Final fallback: No admins confirmed, don't show any
                print(f"[DEBUG] No admin entities confirmed from {len(entities)} total entities")
                self.available_entities = []
                self.entity_cert_mapping = {}
                self.admin_display_names = []
                self.display_name_to_cert_name = {}
            else:
                # If no valid certificates were found, add sample entities
                print("[DEBUG] No valid certificates found, using sample entities")
                self.available_entities = [
                    "Entity A",
                    "Entity B",
                    "Entity C",
                    "Entity D",
                ]
                # Create sample entity mapping for testing
                self.entity_cert_mapping = {
                    "Entity A": "",
                    "Entity B": "",
                    "Entity C": "",
                    "Entity D": "",
                }

        except Exception as e:
            print(f"Error loading certificates: {str(e)}")
            # Add some sample entities for demonstration
            print("[DEBUG] Exception occurred, using sample entities")
            self.available_entities = ["Entity A", "Entity B", "Entity C", "Entity D"]
            # Create sample entity mapping for testing
            self.entity_cert_mapping = {
                "Entity A": "",
                "Entity B": "",
                "Entity C": "",
                "Entity D": "",
            }
