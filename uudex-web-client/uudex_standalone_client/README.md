# UUDEX Standalone CLI

A colorful and feature-rich standalone command-line interface for the UUDEX API. This CLI provides certificate-based authentication, table output, and supports various UUDEX API operations.

## Features

- 🎨 **Colorful Interface**: Built with Rich library for beautiful terminal output
- 📊 **Table Display**: Data displayed in formatted tables with multiple output formats
- 🔐 **Certificate Authentication**: Secure authentication using X.509 certificates
- 📋 **Multiple Output Formats**: Support for table, JSON, and tree output formats
- 🚀 **Comprehensive API Coverage**: Access to endpoints, datasets, subjects, and subscriptions

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have the uudex-api-client available in the parent directory or install it:
```bash
pip install -e ../uudex-api-client
```

## Configuration

The CLI uses environment variables for configuration:

- `CERTS_DIR`: Directory containing X.509 certificates (default: `./certs`)
- `UUDEX_BASE_URL`: Base URL for the UUDEX API (default: `https://localhost`)
- `UUDEX_API_VERSION`: API version (default: `v1`)
- `DEBUG_MODE`: Enable debug mode (default: `false`)

## Certificate Setup

Place your X.509 certificates in the certificates directory:

```
certs/
├── ca.crt              # Certificate Authority certificate
├── entity1.crt         # Entity 1 certificate
├── entity1.key         # Entity 1 private key
├── entity2.crt         # Entity 2 certificate
├── entity2.key         # Entity 2 private key
└── ...
```

The CLI will automatically discover entities from the certificate Common Names.

## Usage

### Basic Usage

```bash
# Show help
python cli.py --help

# List available entities
python cli.py entities

# Check API status
python cli.py status

# Show configuration
python cli.py config-info
```

### Entity Selection

```bash
# Use specific entity
python cli.py -e "entity_name" endpoints list

# Interactive entity selection (if no entity specified)
python cli.py endpoints list
```

### Output Formats

```bash
# Table output (default)
python cli.py endpoints list

# JSON output
python cli.py -o json endpoints list

# Tree output
python cli.py -o tree endpoints list
```

### Endpoint Management

```bash
# List all endpoints
python cli.py endpoints list

# Get specific endpoint details
python cli.py endpoints get <endpoint_uuid>

# List peer endpoints
python cli.py endpoints peers

# Get current endpoint info
python cli.py endpoints me
```

### Dataset Management

```bash
# List datasets for a subject
python cli.py datasets list <subject_uuid>

# List datasets with search filter
python cli.py datasets list <subject_uuid> --search "filter_expression"

# Get specific dataset
python cli.py datasets get <dataset_uuid>
```

### Subject Management

```bash
# Discover available subjects
python cli.py subjects discover

# Filter subjects by name
python cli.py subjects discover --name "subject_name"

# Get specific subject details
python cli.py subjects get <subject_uuid>
```

### Subscription Management

```bash
# List all subscriptions
python cli.py subscriptions list

# Consume messages from subscription
python cli.py subscriptions consume <subscription_uuid>

# Limit number of messages consumed
python cli.py subscriptions consume <subscription_uuid> --max-messages 5
```

## Examples

### Check API Status
```bash
python cli.py status
```

### List Endpoints with Specific Entity
```bash
python cli.py -e "alice" endpoints list
```

### Get Dataset Information in JSON Format
```bash
python cli.py -o json datasets get <dataset_uuid>
```

### Discover Subjects with Verbose Output
```bash
python cli.py -v subjects discover
```

## Error Handling

The CLI provides comprehensive error handling with colored output:

- 🟢 **Green**: Success messages
- 🔴 **Red**: Error messages
- 🟡 **Yellow**: Warning messages
- 🔵 **Blue**: Information messages

## Troubleshooting

### Common Issues

1. **Certificate not found**: Ensure certificates are in the correct directory and have proper permissions
2. **Authentication failed**: Verify certificate and key files are valid and match
3. **API connection failed**: Check network connectivity and API URL configuration
4. **No entities found**: Ensure certificate directory contains valid X.509 certificates

### Debug Mode

Enable debug mode for detailed output:
```bash
export DEBUG_MODE=true
python cli.py status
```

## Development

### Project Structure

```
uudex_standalone_client/
├── cli.py              # Main CLI application
├── cert_manager.py     # Certificate management
├── config.py          # Configuration management
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

### Contributing

1. Follow PEP 8 style guidelines
2. Add type hints for all functions
3. Include comprehensive error handling
4. Update documentation for new features
