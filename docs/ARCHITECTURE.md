# Architecture Documentation

## Overview

SSF Transmitter is built using a modular, production-grade architecture that separates concerns and promotes maintainability, testability, and scalability.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client                               │
│                    (Web Browser)                            │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/HTTPS
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Application                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           API Layer (routes.py)                      │  │
│  │  • REST endpoints                                    │  │
│  │  • Request validation                                 │  │
│  │  • Response formatting                                │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │           Core Business Logic                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │ Event Types  │  │ JWT Handler  │  │ Key Manager│ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │           Services Layer                             │  │
│  │  • Okta Client                                        │  │
│  │  • External integrations                              │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Okta Platform                               │
│              (SSF Event Receiver)                           │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
ssf-transmitter/
├── src/ssf_transmitter/          # Application package
│   ├── __init__.py              # Package initialization
│   ├── app.py                   # Flask app factory
│   ├── config.py                # Configuration management
│   │
│   ├── api/                     # API Layer
│   │   ├── __init__.py
│   │   └── routes.py            # REST endpoints
│   │
│   ├── core/                    # Business Logic
│   │   ├── __init__.py
│   │   ├── event_types.py       # Event type definitions
│   │   ├── jwt_handler.py       # JWT/SET generation
│   │   └── key_manager.py       # RSA key management
│   │
│   ├── services/                # External Services
│   │   ├── __init__.py
│   │   └── okta_client.py       # Okta API client
│   │
│   ├── utils/                   # Utilities
│   │   ├── __init__.py
│   │   └── validators.py        # Validation functions
│   │
│   ├── templates/               # HTML templates
│   │   └── index.html
│   │
│   └── static/                  # Static assets
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_api.py             # API tests
│   └── test_core.py            # Core logic tests
│
├── scripts/                     # Utility scripts
│   ├── dev.sh                  # Development server
│   ├── start.sh                # Production server
│   └── test.sh                 # Test runner
│
├── docs/                        # Documentation
│   ├── README.md               # Docs index
│   ├── ARCHITECTURE.md         # This file
│   ├── QUICK_START.md          # Quick start
│   ├── RAILWAY_DEPLOYMENT.md   # Deployment guide
│   └── ...
│
├── certs/                       # Certificates (auto-generated)
│   ├── private_key.pem
│   └── public_key.pem
│
├── wsgi.py                      # WSGI entry point
├── setup.py                     # Package setup
├── requirements.txt             # Dependencies
├── Dockerfile                   # Docker config
├── Makefile                     # Build automation
├── pytest.ini                   # Pytest config
└── .env.example                 # Environment template
```

## Layer Responsibilities

### 1. API Layer (`api/`)

**Purpose:** Handle HTTP requests and responses

**Responsibilities:**
- Define REST endpoints
- Validate incoming requests
- Format responses
- Handle errors gracefully
- Route requests to appropriate services

**Files:**
- `routes.py` - Blueprint with all routes

**Key Endpoints:**
- `GET /` - Web UI
- `GET /.well-known/jwks.json` - JWKS public keys
- `GET /api/config` - Public configuration
- `GET /api/event-types` - Available event types
- `POST /api/send-event` - Send security event
- `GET /health` - Health check

### 2. Core Layer (`core/`)

**Purpose:** Implement business logic

**Responsibilities:**
- Define event types
- Generate and sign JWTs/SETs
- Manage cryptographic keys
- Implement domain logic
- Maintain data models

**Files:**
- `event_types.py` - SSF event type definitions
- `jwt_handler.py` - JWT/SET generation and signing
- `key_manager.py` - RSA key pair management

**Key Classes:**
- `KeyManager` - RSA key generation and JWKS creation
- `JWTHandler` - SET token generation and signing

### 3. Services Layer (`services/`)

**Purpose:** Integrate with external services

**Responsibilities:**
- Make external API calls
- Handle service-specific protocols
- Manage authentication
- Handle retries and errors
- Abstract external dependencies

**Files:**
- `okta_client.py` - Okta API integration

**Key Classes:**
- `OktaClient` - Send SETs to Okta

### 4. Utils Layer (`utils/`)

**Purpose:** Provide common utilities

**Responsibilities:**
- Validation functions
- Helper functions
- Common operations
- Shared utilities

**Files:**
- `validators.py` - Email, URL, payload validation

### 5. Configuration (`config.py`)

**Purpose:** Manage application configuration

**Responsibilities:**
- Environment variable loading
- Configuration classes per environment
- Default values
- Validation of config

**Configuration Classes:**
- `Config` - Base configuration
- `DevelopmentConfig` - Development settings
- `ProductionConfig` - Production settings
- `TestingConfig` - Test settings

### 6. Application Factory (`app.py`)

**Purpose:** Create and configure Flask app

**Responsibilities:**
- Initialize Flask application
- Load configuration
- Setup logging
- Register blueprints
- Initialize services
- Configure middleware (CORS)

**Key Function:**
- `create_app(config_name)` - Application factory

## Data Flow

### Sending a Security Event

```
1. User fills form in Web UI
   │
   ▼
2. JavaScript sends POST to /api/send-event
   {
     "subject": "user@example.com",
     "eventType": "CREDENTIAL_CHANGE_REQUIRED",
     "reason": "Password compromised"
   }
   │
   ▼
3. API Layer validates request
   - Check required fields
   - Validate email format
   - Validate event type
   │
   ▼
4. Core Layer generates SET
   - Get event URI
   - Create JWT payload
   - Add subject and reason
   - Load private key
   - Sign with RS256
   │
   ▼
5. Services Layer sends to Okta
   - POST to Okta endpoint
   - Content-Type: application/secevent+jwt
   - Handle response
   │
   ▼
6. API Layer returns response
   {
     "success": true,
     "status": 202,
     "data": { ... }
   }
   │
   ▼
7. UI displays result to user
```

### JWKS Endpoint

```
1. Client requests /.well-known/jwks.json
   │
   ▼
2. API Layer receives request
   │
   ▼
3. Key Manager loads public key
   │
   ▼
4. Key Manager converts to JWKS format
   {
     "keys": [{
       "kty": "RSA",
       "use": "sig",
       "kid": "transmitter-key-1",
       "alg": "RS256",
       "n": "...",
       "e": "AQAB"
     }]
   }
   │
   ▼
5. API Layer returns JWKS
```

## Security Architecture

### Key Management

```
┌─────────────────────────────────────────────┐
│           Key Manager                        │
│  ┌────────────────────────────────────────┐ │
│  │  Private Key (private_key.pem)         │ │
│  │  • Generated on first startup          │ │
│  │  • Stored in certs/ directory          │ │
│  │  • Used for signing SETs               │ │
│  │  • Never exposed                        │ │
│  └────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────┐ │
│  │  Public Key (public_key.pem)           │ │
│  │  • Derived from private key            │ │
│  │  • Exposed via JWKS endpoint           │ │
│  │  • Used by Okta for verification       │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### JWT/SET Structure

```json
{
  "header": {
    "alg": "RS256",
    "kid": "transmitter-key-1",
    "typ": "secevent+jwt"
  },
  "payload": {
    "iss": "https://your-app.railway.app",
    "jti": "evt_<uuid>",
    "iat": 1234567890,
    "aud": "https://your-org.okta.com",
    "events": {
      "https://schemas.openid.net/secevent/risc/event-type/...": {
        "subject": {
          "format": "email",
          "email": "user@example.com"
        },
        "reason": "..."
      }
    }
  },
  "signature": "..."
}
```

## Testing Architecture

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
│   • app fixture            # Flask test app
│   • client fixture         # Test client
│   • temp_keys fixture      # Temporary keys
│   • jwt_handler fixture    # JWT handler
│
├── test_api.py              # API endpoint tests
│   • Health check
│   • JWKS endpoint
│   • Config endpoint
│   • Event types
│   • Send event validation
│   • Main page
│
└── test_core.py             # Core logic tests
    • Event types
    • JWT generation
    • Key management
    • JWKS generation
```

### Testing Strategy

1. **Unit Tests** - Test individual components
2. **Integration Tests** - Test component interactions
3. **API Tests** - Test HTTP endpoints
4. **Fixture-based** - Reusable test components

## Deployment Architecture

### Docker Container

```
┌─────────────────────────────────────────┐
│        Docker Container                  │
│  ┌────────────────────────────────────┐ │
│  │  Gunicorn (WSGI Server)            │ │
│  │  • 4 workers                        │ │
│  │  • 30s timeout                      │ │
│  │  • Graceful restart                 │ │
│  └────────────┬───────────────────────┘ │
│               │                          │
│  ┌────────────▼───────────────────────┐ │
│  │  Flask Application                  │ │
│  │  • wsgi.py entry point             │ │
│  │  • Production config                │ │
│  │  • Logging configured               │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  File System                        │ │
│  │  /app/                              │ │
│  │  ├── src/                           │ │
│  │  ├── certs/ (keys generated here)  │ │
│  │  └── wsgi.py                        │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Railway Platform

```
┌─────────────────────────────────────────────┐
│           Railway Platform                   │
│  ┌────────────────────────────────────────┐ │
│  │  Load Balancer                          │ │
│  │  • HTTPS termination                    │ │
│  │  • Domain routing                       │ │
│  └────────────┬───────────────────────────┘ │
│               │                              │
│  ┌────────────▼───────────────────────────┐ │
│  │  Container Instance                     │ │
│  │  • Auto-scaling                         │ │
│  │  • Health monitoring                    │ │
│  │  • Log aggregation                      │ │
│  └────────────┬───────────────────────────┘ │
│               │                              │
│  ┌────────────▼───────────────────────────┐ │
│  │  Environment Variables                  │ │
│  │  • ISSUER                               │ │
│  │  • OKTA_DOMAIN                          │ │
│  │  • KEY_ID                               │ │
│  │  • PORT                                 │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Logging Architecture

### Log Levels

- **DEBUG** - Detailed diagnostic info (development only)
- **INFO** - General informational messages
- **WARNING** - Warning messages
- **ERROR** - Error messages
- **CRITICAL** - Critical errors

### Log Format

```
[2024-03-29 02:00:00,000] INFO in module_name: Message
```

### Logged Events

- Application startup
- Configuration loaded
- Keys generated/loaded
- Event transmissions
- API requests
- Errors and exceptions

## Performance Considerations

### Optimization Strategies

1. **Caching**
   - Public key cached in memory
   - Configuration cached in app context

2. **Connection Pooling**
   - Requests library handles connection pooling

3. **Async Processing** (Future Enhancement)
   - Queue-based event processing
   - Background workers

4. **Resource Management**
   - Gunicorn workers for concurrency
   - Worker timeout configuration

### Scalability

- **Horizontal Scaling** - Add more container instances
- **Vertical Scaling** - Increase container resources
- **Load Balancing** - Railway handles automatically

## Error Handling

### Error Flow

```
Error occurs
   │
   ▼
Logged with context
   │
   ▼
Formatted response
   │
   ▼
Returned to client
{
  "success": false,
  "error": "Error message",
  "details": "Additional info"
}
```

### Error Types

1. **Validation Errors** - 400 Bad Request
2. **Authentication Errors** - 401 Unauthorized
3. **Not Found** - 404 Not Found
4. **Server Errors** - 500 Internal Server Error

## Future Enhancements

### Planned Features

1. **Authentication**
   - API key authentication
   - OAuth 2.0 integration

2. **Event History**
   - Database for event tracking
   - Event status monitoring

3. **Webhooks**
   - Callback URLs for event status
   - Delivery confirmations

4. **Admin Dashboard**
   - Event analytics
   - Configuration management

5. **Key Rotation**
   - Automated key rotation
   - Zero-downtime key updates

6. **Rate Limiting**
   - Request throttling
   - Abuse prevention

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenID Shared Signals](https://openid.net/wg/sharedsignals/)
- [JWT RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)
- [SET RFC 8417](https://datatracker.ietf.org/doc/html/rfc8417)
- [Okta SSF Documentation](https://developer.okta.com/docs/guides/configure-ssf-receiver/)
