# UUDEX Web Client

A web client for interacting with UUDEX services.

## Setup

```bash
# Install project dependencies
poetry install

# Activate poetry environment (important!)
poetry shell

# Create environment files from examples
cp env.example .env
cp dev.env.example dev.env

# Start the mock API server (required for development)
./scripts/start-mock-server.sh

# Start the web client
ENVFILE=dev.env ./scripts/start-uudex.sh

# Alternative: Reset and start web client (clears .web directory)
./scripts/reset-reflex-app.sh
```

## Development

The project uses:
- Reflex for the web framework
- Poetry for dependency management
- Python-dotenv for environment variables (loaded via rxconfig.py)
- FastAPI for the mock server

### Environment Configuration
- Environment variables are loaded through rxconfig.py
- Default configuration is in .env (copy from env.example)
- Optional: Use ENVFILE environment variable to specify a different config file
  ```bash
  ENVFILE=dev.env reflex run
  ```
- Mock server runs on port 8004
- Web client runs on port 3000

Key environment variables:
```bash
# These are all for reflex itself.
BACKEND_HOST=0.0.0.0    # Host to bind backend server
BACKEND_PORT=8001       # Port for backend server
FRONTEND_PORT=3000      # Port for frontend server
LOGLEVEL=debug         # Logging level
```

### HTTPS Configuration
For secure connections to UUDEX servers, configure the following in your .env:
```bash
# Path to your client certificate and key
UUDEX_CLIENT_CERT=/path/to/client/cert.pem
UUDEX_CLIENT_KEY=/path/to/client/key.pem

# Optional: Custom CA certificate
UUDEX_CA_CERT=/path/to/ca/cert.pem
```

## Components

- Web Client UI (main application)
- Mock API Server (for development and testing)
- UUDEX API Client Integration
  - The application expects a UUDEX API Client implementation
  - Can be configured in two ways:
    1. Install via pip (recommended for production)
    2. Load from local path using UUDEX_API_CLIENT_PATH
  - For development, use the mock server which simulates the API

## Development Setup Notes

### Mock Server

For development, the project includes a mock API server. To use it:

1. Start the mock server:
```bash
./scripts/start-mock-server.sh
```

2. Set environment variables:
```bash
export UUDEX_SERVER_MODE=mock
export UUDEX_API_URL=http://localhost:8004
```

The mock server will run on port 8004 by default.

The mock server provides:
- Test data loaded from fixtures
- API endpoints matching the UUDEX specification
- Health check endpoint at /health
- Configuration endpoints at /mock/*

## Testing

### Running Tests
Run tests with:
```bash
poetry run pytest
```

### Coverage Reports
Run tests with coverage:
```bash
# Generate coverage report
poetry run pytest --cov=uudex_web_client

# Generate HTML coverage report
poetry run pytest --cov=uudex_web_client --cov-report=html

# View the report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
```

Coverage configuration is in pyproject.toml:
- Minimum coverage: 80%
- Excludes test files and __init__.py
- HTML reports show line-by-line coverage
