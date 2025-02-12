#!/usr/bin/env bash

# Exit on error, show commands, error on undefined vars
set -eux

echo "=== Starting Mock Server Setup ==="

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the parent directory
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Using project directory: $PROJECT_DIR ==="

# Change to the project directory
cd "$PROJECT_DIR"

# Kill any existing uvicorn processes on port 8004
echo "=== Cleaning up previous processes ==="
pkill -f "uvicorn.*8004" || true
sleep 1

# Start the mock server
echo "=== Starting mock server on port 8004 ==="
poetry run python -m uvicorn uudex_api_mock_server.server:app --host 0.0.0.0 --port 8004
