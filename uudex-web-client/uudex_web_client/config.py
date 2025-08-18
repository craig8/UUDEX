# uudex_web_client/config.py
import os
from pathlib import Path
from typing import Optional, List


class Config:
    """Configuration for the UUDEX Web Client."""

    def __init__(self):
        """Initialize configuration with environment variables."""
        self.SERVER_MODE = os.getenv("SERVER_MODE", "development")
        self.BACKEND_PORT = int(os.getenv("REFLEX_BACKEND_PORT", "8000"))
        self.UUDEX_PORT = int(os.getenv("UUDEX_PORT", "8004"))

        # Certificate configuration
        self.CERTS_DIR = os.getenv(
            "CERTS_DIR",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "certs"),
        )
        self.DEFAULT_CERT_NAME = os.getenv("DEFAULT_CERT_NAME", "default")

        # Debug mode - only send x-ssl-cert header in debug mode
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
        self.BYPASS_SSL_HEADER = (
            os.getenv("BYPASS_SSL_HEADER", "false").lower() == "true"
        )

    def get_server_url(self) -> str:
        """Get the backend server URL."""
        return f"http://localhost:{self.BACKEND_PORT}"

    def get_uudex_url(self) -> str:
        """Get the UUDEX server URL."""
        return "https://localhost"

    def get_available_certs(self) -> List[str]:
        """Get a list of available certificate names in the certs directory."""
        certs_dir = Path(self.CERTS_DIR)
        if not certs_dir.exists():
            return []

        # Look for .pem or .crt files
        cert_files = list(certs_dir.glob("*.pem")) + list(certs_dir.glob("*.crt"))
        return [cert.stem for cert in cert_files]

    def get_cert_path(self, cert_name: str) -> Optional[str]:
        """Get the full path to a certificate file by name."""
        certs_dir = Path(self.CERTS_DIR)

        # Check for both .pem and .crt extensions
        for ext in [".pem", ".crt"]:
            cert_path = certs_dir / f"{cert_name}{ext}"
            if cert_path.exists():
                return str(cert_path)

        return None


# Create a global instance of the config
uudex_config = Config()
