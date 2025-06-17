import reflex as rx
import os
from typing import List, Dict
from pathlib import Path
from dotenv import load_dotenv
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Load environment variables from .env file
load_dotenv()


class CertificateState(rx.State):
    """Shared state for certificate management."""

    available_entities: List[str] = []
    entity_cert_mapping: Dict[str, str] = {
    }  # Maps entity names to certificate files
    certs_dir: str = os.getenv(
        "CERTS_DIR",
        "./certificates")  # Get directory from env var or use default

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

            # Process each certificate file in the directory
            for cert_file in cert_dir.glob('*.crt'):
                try:
                    with open(cert_file, 'rb') as f:
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
