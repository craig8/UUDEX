"""
UUDEX Standalone Client

A standalone command-line interface for the UUDEX API with certificate-based authentication.
"""

__version__ = "1.0.0"
__author__ = "UUDEX Development Team"
__description__ = "A colorful and feature-rich standalone CLI for the UUDEX API"

from .cert_manager import CertificateManager
from .config import Config

__all__ = ["CertificateManager", "Config"]
