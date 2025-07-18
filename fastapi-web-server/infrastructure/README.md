# Infrastructure Documentation

This directory contains the infrastructure configuration for the UUDEX FastAPI web server project. It includes reverse proxy, SSL/TLS termination, and certificate management.

## Overview

The infrastructure is designed to provide:

- **Reverse Proxy**: Route external requests to internal services
- **SSL/TLS Termination**: Handle HTTPS connections and certificate management
- **Client Certificate Authentication**: Secure API access using client certificates
- **Certificate Management**: Generate and manage CA and client certificates
- **Database Services**: PostgreSQL database and RabbitMQ message broker

## Services

### [Caddy Reverse Proxy](./caddy/README.md)

Caddy serves as the main reverse proxy and handles:

- HTTPS termination with automatic certificate generation
- Client certificate authentication
- Proxying requests to the FastAPI backend on port 8004
- Converting client certificate DN to HTTP headers for backend authentication

**Quick Start:**

```bash
cd caddy
./generate-certs.sh
docker-compose up -d
```

### [PostgreSQL Database Layer](./postgresql/README.md)

PostgreSQL provides the primary data storage with:

- PostgreSQL 14.1 database server
- RabbitMQ message broker for async processing
- Persistent data storage in Docker volumes
- Database initialization scripts

**Quick Start:**

```bash
cd postgresql
docker-compose up -d
```

## Architecture

```text
Internet → Caddy (Port 443) → FastAPI Server (Port 8004)
           ↓                          ↓
    Client Certificate         PostgreSQL (Port 5432)
    Authentication             RabbitMQ (Port 5672)
           ↓
    Certificate DN Headers to Backend
```

## Certificate Management

The infrastructure uses a shared Certificate Authority (CA) for all client certificates. For detailed certificate generation, management, and troubleshooting, see the [Caddy Certificate Management Guide](./caddy/README.md#certificate-management).

## Security Features

- **Mutual TLS (mTLS)**: Both server and client certificates are verified
- **Certificate Validation**: Only certificates signed by the trusted CA are accepted
- **Secure Headers**: Client certificate information passed securely to backend
- **Key Protection**: Private keys are stored with restricted permissions (600)

## Development Workflow

For detailed certificate generation and testing procedures, see the [Caddy README](./caddy/README.md).

**Basic workflow:**

1. Generate certificates: `cd caddy && ./generate-certs.sh`
2. Start infrastructure: `docker-compose up -d`
3. Test connection: See [Caddy testing guide](./caddy/README.md#testing-and-validation)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `UUDEX_CERTS` | Override certificate output directory | `certs` |

## Monitoring and Logs

- **Caddy Admin API**: Available on port 2019
- **Docker Logs**: `docker-compose logs -f caddy`
- **Certificate Status**: `./generate-certs.sh --list`

## Troubleshooting

For comprehensive troubleshooting, see the [Caddy Troubleshooting Guide](./caddy/README.md#troubleshooting).

### Quick Infrastructure Check

```bash
# Check if Caddy services are running
docker-compose -f caddy/docker-compose.yml ps

# Check if database services are running
docker-compose -f postgresql/docker-compose.yml ps

# View Caddy logs
docker-compose -f caddy/docker-compose.yml logs -f

# View database logs
docker-compose -f postgresql/docker-compose.yml logs -f
```

## Service Dependencies

- **Docker**: Required for containerized services
- **OpenSSL**: Required for certificate generation
- **FastAPI Backend**: Should be running on port 8004

## Next Steps

1. Set up additional services (database, monitoring, etc.)
2. Configure production-ready certificates
3. Implement certificate rotation
4. Add monitoring and alerting

For detailed service-specific documentation, see the individual README files in each service directory.
