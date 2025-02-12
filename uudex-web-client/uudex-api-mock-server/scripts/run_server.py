#!/usr/bin/env python3
import uvicorn
from uudex_api_mock_server import app
import os


def main():
    port = int(os.getenv("UUDEX_MOCK_SERVER_PORT", "8004"))
    host = os.getenv("UUDEX_MOCK_SERVER_HOST", "0.0.0.0")

    print(f"Starting UUDEX Mock Server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
