# SSF Receiver

Receive and process Security Event Tokens (SETs) from Okta.

## Overview

The SSF Receiver accepts SETs sent by Okta's transmitter and logs them in a formatted, easy-to-read format.

## Features

- ✅ Receives SETs via HTTP POST
- ✅ Validates JWT structure
- ✅ Decodes and logs events
- ✅ Formatted console output with boxes
- ✅ Lists all received events
- ✅ Shows user, device, and event details

## Quick Start

### Start Receiver

```bash
./scripts/receiver.sh
```

**Or manually:**
```bash
python receiver_wsgi.py
```

**Access:**
- Receiver endpoint: http://localhost:8081/receive-set
- View events: http://localhost:8081/events
- Health check: http://localhost:8081/health

## Configuration

Set these in `.env`:

```env
RECEIVER_PORT=8081
EXPECTED_ISSUER=https://your-org.okta.com
OKTA_JWKS_URL=https://your-org.okta.com/.well-known/jwks.json
```

## Endpoints

### POST /receive-set
Receives SETs from Okta

**Request:**
```
POST /receive-set
Content-Type: application/secevent+jwt
Body: [JWT Token]
```

**Response:**
```json
{
  "status": "accepted",
  "jti": "evt_..."
}
```
Status: 202 Accepted

### GET /events
List all received events

### POST /events/clear
Clear received events list

### GET /health
Health check

## Log Format

When a SET is received, logs show:

```
================================================================================
📨 RECEIVED SET FROM OKTA
================================================================================
Timestamp: 2024-03-29T19:30:00
Content-Type: application/secevent+jwt
Token length: 847 bytes
--------------------------------------------------------------------------------
JWT HEADER:
{
  "alg": "RS256",
  "kid": "key-1",
  "typ": "secevent+jwt"
}
--------------------------------------------------------------------------------
JWT PAYLOAD:
{
  "iss": "https://your-org.okta.com",
  "jti": "evt_...",
  "aud": "https://your-receiver.com",
  "events": { ... }
}
--------------------------------------------------------------------------------
📋 EVENT DETAILS:
  Issuer: https://your-org.okta.com
  JTI: evt_...
  Issued At: 2024-03-29T19:25:00
  Event Count: 1
--------------------------------------------------------------------------------
🎯 EVENT TYPE: https://schemas.okta.com/secevent/okta/event-type/user-risk-change
  👤 User: john@doe.net
  📱 Device: device-identifier-001
  event_timestamp: 1702448550 (2024-03-29 10:30:00)
  initiating_entity: admin
  reason_admin: {"en": "Event message example"}
  reason_user: {"en": "Event message example"}
  previous_level: low
  current_level: high
================================================================================
✅ SET PROCESSED SUCCESSFULLY
================================================================================
```

## Testing

### Send Test SET to Receiver

```bash
# From transmitter, send to receiver instead of Okta
curl -X POST http://localhost:8081/receive-set \
  -H "Content-Type: application/secevent+jwt" \
  -d "eyJhbGciOiJSUzI1NiIs..."
```

### View Received Events

```bash
curl http://localhost:8081/events
```

## Architecture

```
src/ssf_receiver/
├── api/
│   └── routes.py          API endpoints
├── core/
│   ├── jwt_validator.py   JWT validation
│   └── event_processor.py Event processing
├── services/
│   └── event_logger.py    Formatted logging
├── app.py                 Flask factory
└── config.py              Configuration
```

## Integration

The receiver runs independently from the transmitter:

- **Transmitter:** Port 8080, sends SETs to Okta
- **Receiver:** Port 8081, receives SETs from Okta

Both can run simultaneously for testing end-to-end SSF flow.
