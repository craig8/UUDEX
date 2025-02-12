import os


class TestConfig:
    MOCK_SERVER_URL = "http://localhost:8004"
    REAL_SERVER_URL = os.getenv("UUDEX_API_URL", "http://real-server:8004")

    @classmethod
    def get_server_url(cls, use_real_server: bool = False) -> str:
        return cls.REAL_SERVER_URL if use_real_server else cls.MOCK_SERVER_URL
