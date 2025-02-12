#!/usr/bin/env bash

# Exit on error, show commands, error on undefined vars
set -eux

# Default env file
ENV_FILE=".env"

# Check if env file is provided as argument
if [ $# -eq 1 ]; then
    ENV_FILE="$1"
fi

echo "=== Starting Reflex App Reset ==="

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the parent directory
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Using project directory: $PROJECT_DIR ==="
echo "=== Using env file: $ENV_FILE ==="

# Change to the project directory
cd "$PROJECT_DIR"

# Check if env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: Environment file $ENV_FILE not found"
    exit 1
fi

# Check if mock server is running
echo "=== Checking mock server status ==="
if ! curl -s http://localhost:8004/health > /dev/null 2>&1; then
    echo "ERROR: Mock server is not running on port 8004"
    echo "HINT: Start mock server with: ./scripts/start-mock-server.sh"
    exit 1
fi

echo "=== Mock server is running ==="

# Kill any existing Node processes and clear .web directory
echo "=== Cleaning up previous processes and files ==="
rm -rf "$PROJECT_DIR/.web"

echo "=== Starting Reflex app ==="

# Start the reflex app in the foreground
poetry run reflex run
