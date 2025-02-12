import os
from enum import Enum
from typing import Optional


class ServerMode(Enum):
    MOCK = "mock"
    REAL = "real"


class Config:
    # Server configuration
    SERVER_MODE: ServerMode = ServerMode(os.getenv("UUDEX_SERVER_MODE",
                                                   "mock"))
    MOCK_SERVER_URL: str = os.getenv("UUDEX_API_URL",
                                     "http://localhost:8004/api/v1")
    REAL_SERVER_URL: str = os.getenv("UUDEX_API_URL", "http://localhost:8004")

    @classmethod
    def get_server_url(cls) -> str:
        """Get the appropriate server URL based on mode"""
        return cls.MOCK_SERVER_URL if cls.SERVER_MODE == ServerMode.MOCK else cls.REAL_SERVER_URL
