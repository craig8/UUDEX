# Caddy Reverse Proxy with Client Certificate Authentication

This directory contains the Caddy configuration for the UUDEX FastAPI web server. Caddy serves as a reverse proxy with client certificate authentication, converting client certificates to headers for backend services.

## Quick Start

1. **Generate certificates**:

   ```bash
   chmod +x generate-certs.sh
   ./generate-certs.sh
   ```

2. **Start Caddy**:

   ```bash
   docker-compose up -d
   ```

3. **Test the connection**:

   ```bash
   curl --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://localhost/
   ```

## Configuration Overview

### Caddyfile Configuration

The `Caddyfile` configures Caddy with the following features:

```caddyfile
localhost {
    # Enable TLS with client certificate authentication
    tls {
        client_auth {
            mode require_and_verify
            trusted_ca_cert_file /etc/caddy/ca.crt
        }
    }

    # Proxy to FastAPI server with certificate headers
    reverse_proxy localhost:8004 {
        header_up X-Client-Cert-Subject "{http.request.tls.client.subject}"
        header_up X-Client-Cert-Issuer "{http.request.tls.client.issuer}"
        header_up X-Client-Cert-Serial "{http.request.tls.client.serial}"
    }
}
```

#### Key Features

- **Client Authentication**: `require_and_verify` mode ensures all clients must present valid certificates
- **Certificate Validation**: Only certificates signed by the trusted CA are accepted
- **Header Injection**: Client certificate information is passed to the backend as HTTP headers

### Docker Compose Configuration

The `docker-compose.yml` file configures:

```yaml
services:
  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"      # HTTP (redirects to HTTPS)
      - "443:443"    # HTTPS
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - ./certs:/etc/caddy/certs:ro
      - ./certs/ca-trusted.crt:/etc/caddy/ca.crt:ro
      - ./certs/ca-trusted.crt:/etc/caddy/ca-trusted.crt:ro
    environment:
      - CADDY_ADMIN=0.0.0.0:2019  # Admin API endpoint
```

#### Volume Mounts

- **Caddyfile**: Configuration file (read-only)
- **Certificate Directory**: All certificates accessible to Caddy
- **CA Certificate**: Specific mount for trusted CA certificate at `/etc/caddy/ca.crt`
- **CA Trusted Certificate**: Additional mount for CA certificate at `/etc/caddy/ca-trusted.crt` (required by Caddyfile trust_pool configuration)

## Certificate Management

### Generate Certificates Script

The `generate-certs.sh` script provides comprehensive certificate management with support for multiple domains:

#### Basic Usage

```bash
# Generate default client certificate (with localhost server certificate)
./generate-certs.sh

# Generate certificate for specific client
./generate-certs.sh alice

# Generate certificate with custom organization
./generate-certs.sh bob "Acme Corporation"
```

#### Multi-Domain Server Certificates

```bash
# Generate server certificate for multiple domains only
./generate-certs.sh --server-only "My Organization" --domain localhost --domain api.example.com

# Generate server certificate with wildcard domains
./generate-certs.sh --server-only "Acme Corp" --domain "*.example.com" --domain example.com

# Generate client certificate with custom server domains
./generate-certs.sh alice "My Org" --domain localhost --domain api.local --domain test.local
```

#### Advanced Options

```bash
# Custom certificate parameters
./generate-certs.sh alice "Acme Corp" \
  --country CA \
  --state Ontario \
  --city Toronto \
  --days 730 \
  --key-size 2048 \
  --domain api.acme.com \
  --domain *.dev.acme.com

# Custom output directory
./generate-certs.sh bob "Beta Inc" --output-dir /custom/path

# List existing certificates
./generate-certs.sh --list
```

#### Environment Variables

```bash
# Override default certificate directory
export UUDEX_CERTS=/custom/cert/path
./generate-certs.sh alice
```

#### Command-Line Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--domain DOMAIN` | Add domain to server certificate (can be used multiple times) | `--domain api.example.com` |
| `--server-only` | Generate only server certificate, no client certificate | `--server-only "My Org"` |
| `--list` | List all existing certificates | `--list` |
| `-c, --country CODE` | Country code for certificates | `--country CA` |
| `-s, --state STATE` | State or province | `--state Ontario` |
| `-l, --city CITY` | City or locality | `--city Toronto` |
| `-d, --days DAYS` | Certificate validity in days | `--days 730` |
| `-k, --key-size SIZE` | RSA key size in bits | `--key-size 2048` |
| `-o, --output-dir DIR` | Custom output directory | `--output-dir /tmp/certs` |
| `-h, --help` | Show help message | `--help` |

#### Usage Patterns

```bash
# Client + Server mode (default)
./generate-certs.sh [CLIENT_NAME] [ORG] [OPTIONS]

# Server-only mode
./generate-certs.sh --server-only [ORG] --domain DOMAIN1 [--domain DOMAIN2...]

# List certificates
./generate-certs.sh --list
```

### Certificate Files Generated

For each client, the following files are created:

- **`{client}.crt`**: Client certificate (PEM format)
- **`{client}.key`**: Client private key (PEM format)
- **`{client}.p12`**: Client certificate bundle (PKCS#12 format for browsers)

### CA Files

- **`ca.crt`**: Certificate Authority certificate
- **`ca.key`**: CA private key (kept secure)
- **`ca-trusted.crt`**: Copy of CA certificate for Caddy

### Server Files

- **`localhost.crt`**: Server certificate for localhost only (backward compatibility)
- **`localhost.key`**: Server private key for localhost
- **`server.crt`**: Multi-domain server certificate (when multiple domains specified)
- **`server.key`**: Multi-domain server private key

**Note**: The script automatically chooses between `localhost.crt` and `server.crt` based on domains:
- Single domain "localhost" → `localhost.crt` (backward compatibility)
- Multiple domains or non-localhost domains → `server.crt` with Subject Alternative Names (SAN)

## Testing and Validation

### Test with curl

```bash
# Basic test with default localhost certificate
curl --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://localhost/

# Test with multi-domain server certificate
curl --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://api.example.com/

# Test different domains from same certificate (if server.crt has SAN)
curl --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://api.local/
curl --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://test.local/

# Verify certificate domains
openssl x509 -in certs/server.crt -text -noout | grep "DNS:"

# If running from a different directory, use full paths
curl --cacert /path/to/infrastructure/caddy/certs/ca.crt --cert /path/to/infrastructure/caddy/certs/alice.crt --key /path/to/infrastructure/caddy/certs/alice.key https://localhost/

# Verify certificate files exist before testing
ls -la certs/
# Expected output may show (depending on generation options):
# -rw-r--r-- 1 user user 1234 Dec  1 12:00 ca.crt
# -rw-r--r-- 1 user user 1234 Dec  1 12:00 ca-trusted.crt
# -rw-r--r-- 1 user user 1234 Dec  1 12:00 server.crt      # Multi-domain server cert
# -rw------- 1 user user 3456 Dec  1 12:00 server.key      # Multi-domain server key
# -rw-r--r-- 1 user user 1234 Dec  1 12:00 localhost.crt   # OR single localhost cert
# -rw------- 1 user user 3456 Dec  1 12:00 localhost.key   # OR single localhost key
# -rw-r--r-- 1 user user 1234 Dec  1 12:00 alice.crt
# -rw------- 1 user user 3456 Dec  1 12:00 alice.key
# -rw-r--r-- 1 user user 1234 Dec  1 12:00 alice.p12

# Expected output (if FastAPI backend is running):
# {"message":"Hello World","certificate_info":{"subject":"CN=alice,O=Acme Corp,C=US",...}}

# Verbose output to see TLS negotiation
curl -v --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://localhost/

# Expected output includes TLS handshake details:
# * TLSv1.3 (OUT), TLS handshake, Client hello (1):
# * TLSv1.3 (IN), TLS handshake, Server hello (2):
# * TLSv1.3 (IN), TLS handshake, Certificate (11):
# * TLSv1.3 (OUT), TLS handshake, Certificate (11):
# * TLSv1.3 (OUT), TLS handshake, Certificate verify (15):
# * SSL connection using TLSv1.3 / TLS_AES_128_GCM_SHA256
# * Server certificate:
# *  subject: CN=localhost
# {"message":"Hello World"}

# Test with custom client certificate
curl --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://localhost/

# Expected output:
# {"message":"Hello authenticated client","subject":"CN=alice,O=Acme Corp,C=US"}

# Test without client certificate (should fail)
curl --cacert certs/ca.crt https://localhost/

# Expected output:
# curl: (35) error:14094412:SSL routines:ssl3_read_bytes:sslv3 alert bad certificate
# OR
# curl: (35) Peer reports incompatible or unsupported protocol version

# Test with invalid certificate (should fail)
curl -k --cert invalid.crt --key invalid.key https://localhost/

# Expected output:
# curl: (35) error:14094418:SSL routines:ssl3_read_bytes:tlsv1 alert unknown ca

# Test headers being passed to backend
curl --cacert certs/ca.crt --cert certs/client.crt --key certs/client.key https://localhost/headers

# Expected output (if backend has /headers endpoint):
# {
#   "x-client-cert-subject": "CN=client,O=Organization,C=US",
#   "x-client-cert-issuer": "CN=LocalCA,O=Organization,C=US",
#   "x-client-cert-serial": "123456789"
# }

# For production: Extract and use Caddy's server certificate
echo | openssl s_client -connect localhost:443 -servername localhost 2>/dev/null | openssl x509 > caddy-server.crt
curl --cacert caddy-server.crt --cert certs/alice.crt --key certs/alice.key https://localhost/
```

### Common Usage Examples

#### Development Environment (localhost only)
```bash
# Generate client certificate with default localhost server certificate
./generate-certs.sh alice "Dev Team"

# Test with localhost
curl --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://localhost/
```

#### Multi-Domain Development
```bash
# Generate server certificate for multiple development domains
./generate-certs.sh bob "Acme Corp" --domain localhost --domain api.local --domain admin.local

# Test different domains
curl --cacert certs/ca.crt --cert certs/bob.crt --key certs/bob.key https://localhost/
curl --cacert certs/ca.crt --cert certs/bob.crt --key certs/bob.key https://api.local/
```

#### Production-Like Environment
```bash
# Generate server certificate for production domains
./generate-certs.sh --server-only "Production Org" \
  --domain api.example.com \
  --domain admin.example.com \
  --domain "*.staging.example.com"

# Generate client certificates for different users
./generate-certs.sh admin "Production Org"
./generate-certs.sh service-account "Production Org"

# Test with production domains (assuming DNS/hosts file setup)
curl --cacert certs/ca.crt --cert certs/admin.crt --key certs/admin.key https://api.example.com/
```

#### Microservices Environment
```bash
# Server certificate covering all service domains
./generate-certs.sh --server-only "Microservices Inc" \
  --domain gateway.service.local \
  --domain auth.service.local \
  --domain user.service.local \
  --domain order.service.local

# Individual service accounts
./generate-certs.sh gateway-service "Microservices Inc"
./generate-certs.sh auth-service "Microservices Inc"
./generate-certs.sh user-service "Microservices Inc"
```

#### Certificate Inspection
```bash
# List all certificates
./generate-certs.sh --list

# View certificate details
openssl x509 -in certs/server.crt -text -noout

# Check Subject Alternative Names
openssl x509 -in certs/server.crt -text -noout | grep -A 3 "Subject Alternative Name"

# Verify certificate chain
openssl verify -CAfile certs/ca.crt certs/alice.crt
```

### Browser Testing

1. Import `certs/alice.p12` (or your client certificate's p12 file) into your browser
2. Password: `changeme`
3. Navigate to `https://localhost` (or your configured domain)
4. Select the client certificate when prompted

**Expected browser behavior:**

- Browser prompts for certificate selection
- Page loads successfully showing FastAPI response
- Browser address bar shows secure connection (lock icon)
- Certificate details available in browser security info

**Multi-Domain Testing:**
If you generated a multi-domain server certificate, you can test different domains:
- `https://localhost/`
- `https://api.example.com/` (if configured in certificate and DNS/hosts)
- `https://admin.example.com/` (if configured in certificate and DNS/hosts)

### Validate Certificates

```bash
# Check certificate validity
openssl x509 -in certs/client.crt -text -noout

# Expected output includes:
# Certificate:
#     Data:
#         Version: 3 (0x2)
#         Serial Number: 123456789
#         Signature Algorithm: sha256WithRSAEncryption
#         Issuer: C=US, ST=State, L=City, O=Organization, CN=LocalCA
#         Validity
#             Not Before: Dec  1 00:00:00 2024 GMT
#             Not After : Dec  1 00:00:00 2025 GMT
#         Subject: C=US, ST=State, L=City, O=Organization, CN=client

# Verify certificate chain
openssl verify -CAfile certs/ca.crt certs/client.crt

# Expected output:
# certs/client.crt: OK

# Check certificate expiration
openssl x509 -in certs/client.crt -noout -enddate

# Expected output:
# notAfter=Dec  1 00:00:00 2025 GMT
```

## Backend Integration

### Headers Sent to Backend

Caddy automatically adds these headers to requests forwarded to the backend:

| Header | Description | Example |
|--------|-------------|---------|
| `X-Client-Cert-Subject` | Certificate subject DN | `CN=alice,O=Acme Corp,C=US` |
| `X-Client-Cert-Issuer` | Certificate issuer DN | `CN=LocalCA,O=Acme Corp,C=US` |
| `X-Client-Cert-Serial` | Certificate serial number | `123456789` |

### FastAPI Backend Example

```python
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/")
async def root(
    x_client_cert_subject: str = Header(None, alias="X-Client-Cert-Subject"),
    x_client_cert_issuer: str = Header(None, alias="X-Client-Cert-Issuer"),
    x_client_cert_serial: str = Header(None, alias="X-Client-Cert-Serial")
):
    if not x_client_cert_subject:
        raise HTTPException(status_code=401, detail="Client certificate required")

    return {
        "message": "Hello authenticated client",
        "subject": x_client_cert_subject,
        "issuer": x_client_cert_issuer,
        "serial": x_client_cert_serial
    }
```

## Troubleshooting

### Quick Diagnostics

First, check if Caddy is running properly:

```bash
# Check container status
docker ps | grep caddy

# If Caddy is constantly restarting, check logs for errors
docker logs caddy-proxy

# Test basic connectivity
curl -I https://localhost/ --insecure
```

### Common Connection Issues

#### 1. "Connection refused" on port 443

**Symptoms**: `curl: (7) Failed to connect to localhost port 443`

**Causes & Solutions**:

- **Caddy not running**: `docker-compose up -d`
- **Port conflict**: Check if another service uses port 443: `sudo lsof -i :443`
- **Firewall blocking**: Ensure port 443 is open
- **Docker networking**: Verify port mapping in `docker-compose.yml`

#### 2. "SSL certificate verification failed"

**Symptoms**: `curl: (60) SSL certificate problem: unable to get local issuer certificate`

**Solutions**:

```bash
# Use the CA certificate for verification
curl --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://localhost/

# Or skip verification for testing (not recommended for production)
curl --insecure --cert certs/alice.crt --key certs/alice.key https://localhost/
```

#### 3. "Client certificate required"

**Symptoms**: `curl: (35) error:14094412:SSL routines:ssl3_read_bytes:sslv3 alert bad certificate`

**Solutions**:

```bash
# Ensure you're providing client certificate
curl --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://localhost/

# Check if certificate files exist and are readable
ls -la certs/alice.{crt,key}

# Verify certificate is valid
openssl x509 -in certs/alice.crt -text -noout | grep -A 2 "Validity"
```

### Certificate Management Issues

#### 4. "Certificate files not found"

```bash
# Check current directory
pwd  # Should be: .../infrastructure/caddy

# List available certificates
ls -la certs/

# Generate missing certificates
./generate-certs.sh alice

# Verify certificates were created
ls -la certs/alice.*
```

#### 5. "Permission denied" accessing certificate files

```bash
# Fix certificate permissions
chmod 644 certs/*.crt
chmod 600 certs/*.key

# Verify ownership (if needed)
ls -la certs/
```

#### 6. Expired certificates

```bash
# Check certificate expiration
openssl x509 -in certs/alice.crt -noout -dates

# Regenerate if expired
./generate-certs.sh alice
```

#### 7. Multi-domain certificate issues

**Problem**: Certificate works for localhost but not other domains

**Solutions**:
```bash
# Check which domains are in the server certificate
openssl x509 -in certs/server.crt -text -noout | grep -A 5 "Subject Alternative Name"
# OR
openssl x509 -in certs/localhost.crt -text -noout | grep -A 5 "Subject Alternative Name"

# If no SAN found, regenerate with proper domains
./generate-certs.sh --server-only "My Org" --domain localhost --domain api.example.com

# Verify the certificate now includes all domains
openssl x509 -in certs/server.crt -text -noout | grep "DNS:"
```

**Problem**: Wrong certificate file being used (localhost.crt vs server.crt)

**Solutions**:
```bash
# Check which certificate files exist
ls -la certs/{localhost,server}.{crt,key}

# If you have both, server.crt is the multi-domain one
# Update Caddyfile to use the correct certificate:
# tls /etc/caddy/certs/server.crt /etc/caddy/certs/server.key

# Or regenerate to replace localhost.crt
rm certs/localhost.{crt,key}
./generate-certs.sh alice "My Org" --domain localhost --domain your.domain.com
```
openssl x509 -in certs/alice.crt -noout -dates

# Regenerate if expired
./generate-certs.sh alice
```

### Service Integration Issues

#### 7. "Bad Gateway" or backend connection errors

**Symptoms**: Caddy responds but returns 502/503 errors

**Solutions**:

```bash
# Check if backend service is running
curl http://localhost:8004/

# Verify Docker network connectivity
docker network ls
docker inspect caddy_caddy-network

# Check backend service logs
docker logs [backend-container-name]
```

#### 8. Missing client certificate headers in backend

**Symptoms**: Backend doesn't receive certificate information

**Check**: Ensure Caddyfile has header forwarding configured:

```caddyfile
reverse_proxy host.docker.internal:8004 {
    header_up X-Client-Cert-Subject "{http.request.tls.client.subject}"
    header_up X-Client-Cert-Issuer "{http.request.tls.client.issuer}"
    header_up X-Client-Cert-Serial "{http.request.tls.client.serial}"
}
```

### Container Issues

#### 9. Caddy container keeps restarting

```bash
# Check detailed logs
docker logs caddy-proxy --tail 50

# Common issues and fixes:
# - Configuration syntax error: Validate Caddyfile
# - Missing certificate files: Check volume mounts
# - Permission issues: Verify file permissions
```

#### 10. Configuration validation

```bash
# Test Caddyfile syntax
docker run --rm -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile caddy:2-alpine caddy validate --config /etc/caddy/Caddyfile

# Test with current certificates
docker run --rm \
  -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile:ro \
  -v $(pwd)/certs:/etc/caddy/certs:ro \
  caddy:2-alpine caddy validate --config /etc/caddy/Caddyfile
```

### Debugging Commands

```bash
# Full connection test with verbose output
curl -v --cacert certs/ca.crt --cert certs/alice.crt --key certs/alice.key https://localhost/

# Test TLS handshake
openssl s_client -connect localhost:443 -cert certs/alice.crt -key certs/alice.key -CAfile certs/ca.crt

# Monitor Caddy logs in real-time
docker logs -f caddy-proxy

# Check Caddy admin API status
curl http://localhost:2019/config/ | jq .

# Verify certificate chain
openssl verify -CAfile certs/ca.crt certs/alice.crt
```

### Performance and Monitoring

```bash
# Check Caddy metrics (if enabled)
curl http://localhost:2019/metrics

# Monitor resource usage
docker stats caddy-proxy

# Check connection count
ss -tuln | grep :443
```
