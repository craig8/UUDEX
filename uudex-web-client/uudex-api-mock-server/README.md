# UUDEX API Mock Server

A FastAPI-based mock server for testing UUDEX API clients. This server provides configurable mock endpoints that simulate the behavior of a real UUDEX server.

## Features

- Mock REST API endpoints for UUDEX services
- Configurable responses for testing different scenarios
- Request history tracking
- Built-in support for subscriptions, subjects, and messages
- Easy integration with test suites

## Installation

```bash
# Install from local directory
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Usage

### Starting the Server

There are several ways to start the server:

1. Using the provided script:
```bash
# Make the script executable first
chmod +x scripts/run_server.py

# Run the server
./scripts/run_server.py
```

2. Using Python directly:
```bash
python -m uudex_api_mock_server.scripts.run_server
```

3. Or programmatically:
```python
from uudex_api_mock_server import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
```

### Available Endpoints

#### Mock Control Endpoints
- `POST /mock/reset` - Reset server state
- `POST /mock/configure` - Configure mock responses
- `GET /mock/history` - Get request history

#### UUDEX API Endpoints
- `GET /api/v1/subscriptions` - Get all subscriptions
- `POST /api/v1/subscriptions` - Create subscription
- `DELETE /api/v1/subscriptions/{subscription_id}` - Delete subscription
- `GET /api/v1/subjects` - Get all subjects
- `POST /api/v1/subjects/{subject_id}/messages` - Publish message
- `GET /api/v1/subjects/{subject_id}/messages` - Get messages

### Configuring Mock Responses

```python
import httpx

async def configure_mock_examples():
    async with httpx.AsyncClient() as client:
        # Configure successful response
        await client.post(
            "http://localhost:8004/mock/configure",
            json={
                "path": "api/v1/subscriptions",
                "response": {
                    "id": "sub1",
                    "subject_id": "test/subject",
                    "callback_url": "http://example.com/callback"
                },
                "status_code": 200
            }
        )

        # Configure error response
        await client.post(
            "http://localhost:8004/mock/configure",
            json={
                "path": "api/v1/subscriptions",
                "response": {
                    "detail": "Subscription already exists"
                },
                "status_code": 409
            }
        )
```

### Testing

The server includes a comprehensive test suite:

```bash
# Run all tests
pytest

# Run tests against real server
pytest --use-real-server
```

## Configuration

Environment Variables:
- `UUDEX_MOCK_SERVER_PORT` - Server port (default: 8004)
- `UUDEX_API_URL` - URL for real server when testing with --use-real-server

## Development

Requirements (from setup.py):
- Python 3.10+
- FastAPI >= 0.68.0
- uvicorn >= 0.15.0
- python-multipart >= 0.0.5

Development dependencies:
- pytest >= 6.0.0
- pytest-asyncio >= 0.21.0
- httpx >= 0.18.0

### Local Development Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Keep commits focused and atomic
- Write clear commit messages

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/your-org/uudex-api-mock-server.git
cd uudex-api-mock-server
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

4. Make your changes and run tests:
```bash
pytest
```

## Example Test Client

```python
from uudex_api_mock_server.tests.test_integration import UUDEXTestClient

async def test_example():
    client = UUDEXTestClient(base_url="http://localhost:8004")

    # Configure mock response
    await client.configure_mock(
        path="api/v1/subscriptions",
        response={"id": "test-sub"}
    )

    # Use client
    result = await client.get_subscriptions()

    await client.close()
```

Looking at the current README.md for the mock server, I notice a few things that could be improved:

```markdown:uudex-api-mock-server/README.md
# UUDEX API Mock Server

A FastAPI-based mock server for testing UUDEX API clients. This server provides configurable mock endpoints that simulate the behavior of a real UUDEX server.

## Features

- Mock REST API endpoints for UUDEX services
- Configurable responses for testing different scenarios
- Request history tracking
- Built-in support for subscriptions, subjects, and messages
- Easy integration with test suites

## Installation

```bash
# Install from local directory
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Usage

### Starting the Server

```python
from uudex_api_mock_server import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
```

### Available Endpoints

#### Mock Control Endpoints
- `POST /mock/reset` - Reset server state
- `POST /mock/configure` - Configure mock responses
- `GET /mock/history` - Get request history

#### UUDEX API Endpoints
- `GET /api/v1/subscriptions` - Get all subscriptions
- `POST /api/v1/subscriptions` - Create subscription
- `DELETE /api/v1/subscriptions/{subscription_id}` - Delete subscription
- `GET /api/v1/subjects` - Get all subjects
- `POST /api/v1/subjects/{subject_id}/messages` - Publish message
- `GET /api/v1/subjects/{subject_id}/messages` - Get messages

### Configuring Mock Responses

```python
import httpx

async def configure_mock():
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:8004/mock/configure",
            json={
                "path": "api/v1/subscriptions",
                "response": {
                    "id": "sub1",
                    "subject_id": "test/subject",
                    "callback_url": "http://example.com/callback"
                },
                "status_code": 200
            }
        )
```

### Testing

The server includes a comprehensive test suite:

```bash
# Run all tests
pytest

# Run tests against real server
pytest --use-real-server
```

## Configuration

Environment Variables:
- `UUDEX_MOCK_SERVER_PORT` - Server port (default: 8004)
- `UUDEX_API_URL` - URL for real server when testing with --use-real-server

## Development

Requirements:
- Python 3.7+
- FastAPI
- uvicorn
- pytest (for testing)
- httpx (for testing)

## Example Test Client

```python
from uudex_api_mock_server.tests.test_integration import UUDEXTestClient

async def test_example():
    client = UUDEXTestClient(base_url="http://localhost:8004")

    # Configure mock response
    await client.configure_mock(
        path="api/v1/subscriptions",
        response={"id": "test-sub"}
    )

    # Use client
    result = await client.get_subscriptions()

    await client.close()
```
