# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment files
cp env.example .env
cp dev.env.example dev.env
```

### Running the Application
```bash
# Start mock API server (required for development, runs on port 8004)
./scripts/start-mock-server.sh

# Start web client with default .env
reflex run

# Start with custom environment file
ENVFILE=dev.env ./scripts/start-uudex.sh

# Reset and start (clears .web directory)
./scripts/reset-reflex-app.sh
```

### Testing
```bash
# Run tests (Note: pytest needs to be added to dependencies)
pytest

# Run tests with coverage
pytest --cov=uudex_web_client

# Generate HTML coverage report
pytest --cov=uudex_web_client --cov-report=html
```

## Architecture

### Technology Stack
- **Reflex**: Web framework for building interactive UIs with Python
- **Pip/venv**: Dependency management using virtual environment at `.venv`
- **FastAPI/Uvicorn**: Mock API server for development
- **Python-dotenv**: Environment configuration management

### Project Structure

**Main Application** (`uudex_web_client/`)
- `uudex_web_client.py`: Main app entry point, configures Reflex app with routes
- `state.py`: Application state management using Reflex's State class
- `sender.py`: File sender interface page
- `receiver.py`: File receiver interface page
- `certificate_state.py`: Certificate management state
- `config.py`: Configuration management, loads environment variables

**Mock Server** (`uudex-api-mock-server/`)
- Provides test API endpoints for development
- Runs on port 8004 by default
- Health check at `/health`
- Mock configuration endpoints at `/mock/*`

**Standalone Client** (`uudex_standalone_client/`)
- CLI interface for UUDEX operations
- Certificate management utilities
- Independent from the web client

### Configuration System

Environment variables are loaded through `rxconfig.py` in the following priority:
1. Custom file specified via `ENVFILE` environment variable
2. Default `.env` file
3. System defaults

The configuration flows through:
- `rxconfig.py` loads environment files using python-dotenv
- `uudex_web_client/config.py` provides Config class with parsed settings
- State classes access configuration through the Config instance

### Key Environment Variables
- `BACKEND_HOST`: Backend server host (default: 0.0.0.0)
- `BACKEND_PORT`: Backend server port (default: 8001)
- `FRONTEND_PORT`: Frontend server port (default: 3000)
- `UUDEX_PORT`: UUDEX/Mock API port (default: 8004)
- `CERTS_DIR`: Directory for certificates
- `DEFAULT_CERT_NAME`: Default certificate name
- `DEBUG_MODE`: Enable debug features
- `BYPASS_SSL_HEADER`: Bypass SSL header checks

### State Management

The application uses Reflex's reactive state management:
- Central `State` class in `state.py` manages application data
- `CertificateState` handles certificate-specific operations
- States are reactive - UI updates automatically when state changes
- Event handlers decorated with `@rx.event` for user interactions

### Development Workflow

1. Activate the virtual environment with `source .venv/bin/activate`
2. Mock server must be running before starting the web client
3. The web client checks for mock server availability on startup
4. Environment configuration can be switched using ENVFILE variable
5. The `.web` directory contains generated frontend assets (can be cleared with reset script)

### API Integration

The application supports two modes:
1. **Mock Mode** (development): Uses local mock server on port 8004
2. **Production Mode**: Connects to actual UUDEX servers with SSL certificates

Certificate handling:
- Certificates stored in `certs/` directory
- Supports both `.pem` and `.crt` formats
- Certificate selection available through UI
- SSL verification configurable via environment