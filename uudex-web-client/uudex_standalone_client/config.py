"""
UUDEX Standalone Client - Configuration Management

This module provides configuration management for the UUDEX CLI
without dependencies on the Reflex web client.
"""

import os
from pathlib import Path
from typing import Optional, List


class Config:
    """Configuration for the UUDEX Standalone Client"""

    def __init__(self):
        """Initialize configuration with environment variables"""
        self.SERVER_MODE = os.getenv("SERVER_MODE", "development")
        self.BACKEND_PORT = int(os.getenv("REFLEX_BACKEND_PORT", "8000"))
        self.UUDEX_PORT = int(os.getenv("UUDEX_PORT", "8004"))

        # Certificate configuration
        self.CERTS_DIR = os.getenv("CERTS_DIR",
                                   os.path.join(os.getcwd(), "certs"))
        self.DEFAULT_CERT_NAME = os.getenv("DEFAULT_CERT_NAME", "default")

        # Debug mode
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
        self.BYPASS_SSL_HEADER = os.getenv("BYPASS_SSL_HEADER",
                                           "false").lower() == "true"

        # API configuration
        self.BASE_URL = os.getenv("UUDEX_BASE_URL", "https://localhost")
        self.API_VERSION = os.getenv("UUDEX_API_VERSION", "v1")

    def get_server_url(self) -> str:
        """Get the backend server URL"""
        return f"http://localhost:{self.BACKEND_PORT}"

    def get_uudex_url(self) -> str:
        """Get the UUDEX server URL"""
        return self.BASE_URL

    def get_api_base_url(self) -> str:
        """Get the full API base URL"""
        return f"{self.BASE_URL}/{self.API_VERSION}/uudex"

    def get_available_certs(self) -> List[str]:
        """Get a list of available certificate names in the certs directory"""
        certs_dir = Path(self.CERTS_DIR)
        if not certs_dir.exists():
            return []

        # Look for .pem or .crt files
        cert_files = list(certs_dir.glob("*.pem")) + list(
            certs_dir.glob("*.crt"))
        return [cert.stem for cert in cert_files]

    def get_cert_path(self, cert_name: str) -> Optional[str]:
        """Get the full path to a certificate file by name"""
        certs_dir = Path(self.CERTS_DIR)

        # Check for both .pem and .crt extensions
        for ext in ['.pem', '.crt']:
            cert_path = certs_dir / f"{cert_name}{ext}"
            if cert_path.exists():
                return str(cert_path)

        return None

    def get_key_path(self, cert_name: str) -> Optional[str]:
        """Get the full path to a key file by name"""
        certs_dir = Path(self.CERTS_DIR)

        # Check for .key extension
        key_path = certs_dir / f"{cert_name}.key"
        if key_path.exists():
            return str(key_path)

        return None

    def validate_config(self) -> bool:
        """Validate the configuration"""
        issues = []

        # Check if certificates directory exists
        if not Path(self.CERTS_DIR).exists():
            issues.append(
                f"Certificates directory does not exist: {self.CERTS_DIR}")

        # Check if any certificates are available
        if not self.get_available_certs():
            issues.append("No certificates found in certificates directory")

        if issues:
            print("Configuration validation failed:")
            for issue in issues:
                print(f"  - {issue}")
            return False

        return True

    def print_config(self) -> None:
        """Print current configuration"""
        print("UUDEX Standalone Client Configuration:")
        print(f"  Certificates Directory: {self.CERTS_DIR}")
        print(f"  Base URL: {self.BASE_URL}")
        print(f"  API Base URL: {self.get_api_base_url()}")
        print(f"  Backend Port: {self.BACKEND_PORT}")
        print(f"  UUDEX Port: {self.UUDEX_PORT}")
        print(f"  Debug Mode: {self.DEBUG_MODE}")
        print(f"  Server Mode: {self.SERVER_MODE}")
        print(
            f"  Available Certificates: {', '.join(self.get_available_certs())}"
        )
