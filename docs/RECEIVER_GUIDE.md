# SSF Receiver Guide

## Overview

The SSF Receiver receives Security Event Tokens (SETs) sent by Okta and displays them in beautifully formatted console logs.

---

## 🚀 Quick Start

### 1. Start the Receiver

```bash
./scripts/receiver.sh
```

**The receiver starts on port 8081 (separate from transmitter on 8080)**

### 2. Configure Okta to Send Events

In Okta, configure your transmitter stream to send to:
```
http://localhost:8081/receive-set
```

Or for production:
```
https://your-receiver.railway.app/receive-set
```

### 3. Watch the Logs

When Okta sends a SET, you'll see formatted output in the console!

---

## 📁 Receiver Structure

```
src/ssf_receiver/
├── api/
│   └── routes.py               Receiver endpoints
├── core/
│   ├── jwt_validator.py        JWT validation
│   └── event_processor.py      Event processing
├── services/
│   └── event_logger.py         Formatted logging
├── app.py                      Flask app factory
├── config.py                   Configuration
└── README.md                   Receiver docs

receiver_wsgi.py                Entry point
scripts/receiver.sh             Start script
```

---

## 🔌 Endpoints

### POST /receive-set
**Purpose:** Receive SETs from Okta

**Request:**
```http
POST /receive-set HTTP/1.1
Content-Type: application/secevent+jwt

eyJhbGciOiJSUzI1NiIs...
```

**Response (Success):**
```json
{
  "status": "accepted",
  "jti": "evt_..."
}
```
**Status:** 202 Accepted

**Response (Error):**
```json
{
  "err": "invalid_request",
  "description": "Error details"
}
```
**Status:** 400 Bad Request

---

### GET /events
**Purpose:** List all received events

**Response:**
```json
{
  "total": 5,
  "events": [
    {
      "received_at": "2024-03-29T19:30:00",
      "jti": "evt_...",
      "issuer": "https://your-org.okta.com",
      "event_count": 1,
      "event_types": [
        "https://schemas.okta.com/secevent/okta/event-type/user-risk-change"
      ]
    }
  ]
}
```

---

### POST /events/clear
**Purpose:** Clear received events list

**Response:**
```json
{
  "status": "cleared"
}
```

---

### GET /health
**Purpose:** Health check

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 📊 Log Format

### When SET is Received:

```
================================================================================
📨 RECEIVED SET FROM OKTA
================================================================================
Timestamp: 2024-03-29T19:30:45
Content-Type: application/secevent+jwt
Token length: 1247 bytes
--------------------------------------------------------------------------------
JWT HEADER:
{
  "alg": "RS256",
  "kid": "okta-key-1",
  "typ": "secevent+jwt"
}
--------------------------------------------------------------------------------
JWT PAYLOAD:
{
  "iss": "https://your-org.okta.com",
  "jti": "evt_abc123",
  "aud": "https://your-receiver.com",
  "iat": 1702448550,
  "events": {
    "https://schemas.okta.com/secevent/okta/event-type/user-risk-change": {
      "subject": {
        "user": {"format": "email", "email": "john@doe.net"},
        "device": {"format": "opaque", "id": "device-001"}
      },
      "current_level": "high",
      "previous_level": "low",
      "reason_admin": {"en": "Impossible travel detected"}
    }
  }
}
--------------------------------------------------------------------------------
📋 EVENT DETAILS:
  Issuer: https://your-org.okta.com
  JTI: evt_abc123
  Issued At: 2024-03-29T19:25:00
  Event Count: 1
--------------------------------------------------------------------------------
🎯 EVENT TYPE: https://schemas.okta.com/secevent/okta/event-type/user-risk-change
  👤 User: john@doe.net
  📱 Device: device-001
  event_timestamp: 1702448550 (2024-03-29 10:30:00)
  initiating_entity: admin
  reason_admin: {"en": "Impossible travel detected"}
  previous_level: low
  current_level: high
┌──────────────────────────────────────────────────────────────────────────────┐
│ 👤 User Risk Change                                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│ 🕐 Received: 2024-03-29 19:30:45                                             │
│ 🕐 Issued:   2024-03-29 19:25:00                                             │
│ 🔖 JTI:      evt_abc123                                                      │
│ 👤 User:     john@doe.net                                                    │
│ 📱 Device:   device-001                                                      │
│──────────────────────────────────────────────────────────────────────────────│
│ Event Data:                                                                  │
│   event_timestamp    = 1702448550 (2024-03-29 10:30:00)                     │
│   initiating_entity  = admin                                                 │
│   reason_admin       = {"en": "Impossible travel detected"}                  │
│   previous_level     = low                                                   │
│   current_level      = high                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
================================================================================
✅ SET PROCESSING COMPLETE (Total processed: 1)
================================================================================
```

---

## 🧪 Testing

### Test with Transmitter

**Terminal 1: Start Receiver**
```bash
./scripts/receiver.sh
```

**Terminal 2: Send Test SET**
```bash
# Generate a SET using transmitter and send to receiver
curl -X POST http://localhost:8081/receive-set \
  -H "Content-Type: application/secevent+jwt" \
  -d "$(curl -X POST http://localhost:8080/api/debug-event \
        -H "Content-Type: application/json" \
        -d '{"subject":"test@example.com","eventType":"USER_RISK_CHANGE","device_id":"device-001","current_level":"high","previous_level":"low"}' \
        | jq -r '.jwt_token')"
```

### View Received Events

```bash
curl http://localhost:8081/events | jq
```

---

## 📝 Environment Variables

```env
# Receiver port (default: 8081)
RECEIVER_PORT=8081

# Expected issuer (Okta domain)
EXPECTED_ISSUER=https://your-org.okta.com

# Okta JWKS URL (for signature verification)
OKTA_JWKS_URL=https://your-org.okta.com/.well-known/jwks.json

# Receiver identifier
RECEIVER_ID=ssf-receiver-001
```

---

## 🔒 Security

### Current Implementation:
- ✅ Validates JWT structure
- ✅ Decodes payload
- ⚠️  Signature verification disabled for demo

### Production Recommendations:
1. Enable JWT signature verification
2. Fetch Okta's public keys from JWKS
3. Validate issuer matches expected
4. Add authentication to receiver endpoint
5. Use HTTPS only

---

## 🎯 Use Cases

### 1. Testing SSF Integration
Run receiver locally to test Okta sending SETs

### 2. Debugging Events
See exactly what Okta is sending

### 3. Event Monitoring
Track all security events in real-time

### 4. Development
Test transmitter → receiver flow locally

---

## 📊 Event Types Supported

The receiver can handle all 6 event types:

1. **DEVICE_RISK_CHANGE** - 📱 Device Risk Change
2. **IP_CHANGE** - 🌐 IP Address Change
3. **USER_RISK_CHANGE** - 👤 User Risk Change
4. **DEVICE_COMPLIANCE_CHANGE** - 🔒 Device Compliance Change
5. **SESSION_REVOKED** - 🚪 Session Revoked
6. **IDENTIFIER_CHANGED** - ✉️ Identifier Changed

Each displays with formatted boxes and proper icons!

---

## 🔄 Running Both Transmitter and Receiver

### Terminal 1: Start Transmitter
```bash
./scripts/dev.sh
# Runs on port 8080
```

### Terminal 2: Start Receiver
```bash
./scripts/receiver.sh
# Runs on port 8081
```

### Test Full Flow:
1. Open transmitter UI: http://localhost:8080
2. Send event (it goes to Okta)
3. Configure Okta to forward events to receiver
4. Watch receiver logs for incoming events!

---

## 📚 Additional Resources

- [SSF Receiver Implementation](../ssf_receiver/README.md)
- [RFC 8417 - Security Event Tokens](https://datatracker.ietf.org/doc/html/rfc8417)
- [OpenID Shared Signals](https://openid.net/wg/sharedsignals/)

---

**Receiver is ready to accept SETs from Okta!** 📨
