#!/bin/bash
set -e

# Default port
PORT=${1:-8000}
SERVER_URL="http://localhost:${PORT}"

# Extract version from server pyproject.toml
SERVER_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

echo "Building UUDEX API Client..."
echo "Using server URL: ${SERVER_URL}"
echo "Server version: ${SERVER_VERSION}"

# Check if server is running
if ! curl -s "${SERVER_URL}/openapi.json" > /dev/null 2>&1; then
    echo "Error: UUDEX server not running at ${SERVER_URL}"
    echo "Start the server first with: uvicorn src.uudex_server.main:app --host 0.0.0.0 --port ${PORT}"
    echo ""
    echo "Usage: $0 [PORT]"
    echo "  PORT: Server port (default: 8000)"
    exit 1
fi

# Create generated-client-api directory if it doesn't exist
mkdir -p generated-client-api
cd generated-client-api

echo "Downloading latest OpenAPI specification..."
curl -s "${SERVER_URL}/openapi.json" > openapi.json

# Validate the OpenAPI spec was downloaded
if [ ! -s openapi.json ]; then
    echo "Error: Failed to download OpenAPI specification"
    exit 1
fi

echo "Generating Python API client..."
openapi-python-client update --path ./openapi.json --meta poetry

# Fix ruff configuration and update version to match server
if [ -f "uudex-api-client/pyproject.toml" ]; then
    echo "Fixing ruff configuration and updating version to ${SERVER_VERSION}..."
    # Fix the ruff config structure
    sed -i '/^\[tool\.ruff\]/,/^$/c\
[tool.ruff]\
line-length = 120\
\
[tool.ruff.lint]\
select = ["F", "I", "UP"]' uudex-api-client/pyproject.toml
    
    # Update version to match server
    sed -i "s/^version = .*/version = \"${SERVER_VERSION}\"/" uudex-api-client/pyproject.toml
fi

echo "Installing client dependencies..."
cd uudex-api-client
poetry install

echo "Building client package..."
poetry build
cd ..

echo ""
echo "✅ UUDEX API client built successfully!"
echo ""
echo "The generated client includes all new subject management endpoints:"
echo "  - Complete CRUD operations (create, read, update, delete)"
echo "  - Queue management (info, purge, delete)"
echo "  - Message publishing to subjects"
echo "  - Bulk operations for administrators"
echo "  - Subject discovery and metrics"
echo ""
echo "Client package location: generated-client-api/uudex-api-client/dist/"
echo "To install: pip install generated-client-api/uudex-api-client/dist/uudex_api_client-${SERVER_VERSION}-py3-none-any.whl"