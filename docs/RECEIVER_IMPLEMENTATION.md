# SSF Receiver Implementation - Complete

## ✅ Receiver Successfully Implemented

A complete SSF receiver has been added to receive and log Security Event Tokens from Okta.

---

## 📁 Complete Project Structure

```
src/
├── ssf_transmitter/          Transmitter (Port 8080)
│   ├── api/                  API routes for sending
│   ├── core/                 JWT generation & signing
│   ├── services/             Okta client
│   ├── templates/            Web UI
│   └── static/               CSS, JS
│
└── ssf_receiver/             Receiver (Port 8081) ⭐ NEW!
    ├── api/
    │   └── routes.py         Receiver endpoints
    ├── core/
    │   ├── jwt_validator.py  JWT validation
    │   └── event_processor.py Event processing
    ├── services/
    │   └── event_logger.py   Formatted logging
    ├── app.py               Flask app
    ├── config.py            Configuration
    └── README.md            Receiver docs
```

---

## 🎯 Receiver Features

### 1. **Receive SETs from Okta** 📨
- POST endpoint: `/receive-set`
- Accepts `application/secevent+jwt` content type
- Returns 202 Accepted

### 2. **Formatted Console Logs** 📋
Beautiful boxed output showing:
```
┌──────────────────────────────────────────────────────────────┐
│ 👤 User Risk Change                                          │
├──────────────────────────────────────────────────────────────┤
│ 🕐 Received: 2024-03-29 19:30:45                             │
│ 🕐 Issued:   2024-03-29 19:25:00                             │
│ 🔖 JTI:      evt_abc123                                      │
│ 👤 User:     john@doe.net                                    │
│ 📱 Device:   device-001                                      │
├──────────────────────────────────────────────────────────────┤
│ Event Data:                                                  │
│   event_timestamp    = 1702448550                            │
│   current_level      = high                                  │
│   previous_level     = low                                   │
│   reason_admin       = {"en": "..."}                         │
└──────────────────────────────────────────────────────────────┘
```

### 3. **Event Icons** 🎨
Each event type has a unique icon:
- 📱 Device Risk Change
- 🌐 IP Address Change
- 👤 User Risk Change
- 🔒 Device Compliance Change
- 🚪 Session Revoked
- ✉️ Identifier Changed

### 4. **Event History** 📊
- GET `/events` - List all received events
- POST `/events/clear` - Clear history

### 5. **Health Check** ✅
- GET `/health` - Status check

---

## 🚀 How to Use

### Start Receiver

```bash
./scripts/receiver.sh
```

**Receiver starts on:** http://localhost:8081

**Receive endpoint:** http://localhost:8081/receive-set

### Send Test SET

```bash
# Send a test SET to receiver
curl -X POST http://localhost:8081/receive-set \
  -H "Content-Type: application/secevent+jwt" \
  -d "eyJhbGciOiJSUzI1NiIs..."
```

### View Received Events

```bash
curl http://localhost:8081/events | jq
```

---

## 📊 Console Log Format

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
  "events": { ... }
}
--------------------------------------------------------------------------------
📋 EVENT DETAILS:
  Issuer: https://your-org.okta.com
  JTI: evt_abc123
  Event Count: 1
--------------------------------------------------------------------------------
🎯 EVENT TYPE: user-risk-change
  👤 User: john@doe.net
  📱 Device: device-001
  current_level: high
  previous_level: low
  reason_admin: {"en": "Impossible travel"}
┌──────────────────────────────────────────────────────────────────────────────┐
│ 👤 User Risk Change                                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│ 🕐 Received: 2024-03-29 19:30:45                                             │
│ 👤 User:     john@doe.net                                                    │
│ 📱 Device:   device-001                                                      │
│──────────────────────────────────────────────────────────────────────────────│
│ Event Data:                                                                  │
│   current_level      = high                                                  │
│   previous_level     = low                                                   │
│   reason_admin       = {"en": "Impossible travel"}                           │
└──────────────────────────────────────────────────────────────────────────────┘
================================================================================
✅ SET PROCESSING COMPLETE (Total processed: 1)
================================================================================
```

---

## 🔌 Receiver API

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Receiver status |
| `/receive-set` | POST | Receive SETs from Okta |
| `/events` | GET | List received events |
| `/events/clear` | POST | Clear event history |
| `/health` | GET | Health check |

### Response Codes

- **202 Accepted** - SET received and processed successfully
- **400 Bad Request** - Invalid SET or JWT format
- **500 Server Error** - Processing error

---

## ⚙️ Configuration

Add to `.env`:

```env
# Receiver settings
RECEIVER_PORT=8081
EXPECTED_ISSUER=https://your-org.okta.com
OKTA_JWKS_URL=https://your-org.okta.com/.well-known/jwks.json
RECEIVER_ID=ssf-receiver-001
```

---

## 🧪 Testing

### 1. Start Receiver

```bash
./scripts/receiver.sh
```

### 2. Send Test Event

**Option A: Use transmitter's debug endpoint**
```bash
# Get JWT from debug endpoint
JWT=$(curl -s -X POST http://localhost:8080/api/debug-event \
  -H "Content-Type: application/json" \
  -d '{"subject":"test@example.com","eventType":"USER_RISK_CHANGE","device_id":"device-001","current_level":"high","previous_level":"low"}' \
  | jq -r '.jwt_token')

# Send to receiver
curl -X POST http://localhost:8081/receive-set \
  -H "Content-Type: application/secevent+jwt" \
  -d "$JWT"
```

**Option B: Manually create SET**
Send any valid SET JWT to the receiver endpoint.

### 3. View Logs

Watch the receiver console - you'll see formatted output!

### 4. View Event History

```bash
curl http://localhost:8081/events | jq
```

---

## 📂 File Descriptions

### API Layer
- **routes.py** - HTTP endpoints for receiving SETs

### Core Layer
- **jwt_validator.py** - Validates JWT structure and signature
- **event_processor.py** - Processes and stores received events

### Services Layer
- **event_logger.py** - Formats and logs events to console with boxes

### Configuration
- **config.py** - Environment-based configuration
- **app.py** - Flask application factory

---

## 🎨 Log Features

### Formatted Boxes
- Box drawings with Unicode characters
- Event type icons (📱🌐👤🔒🚪✉️)
- Timestamp conversions
- Color-coded output (via logging levels)

### Detailed Information
- JWT header and payload
- Event metadata (iss, jti, iat)
- Subject details (user + device)
- All event-specific fields
- Timestamps in human-readable format

### Event Counter
- Tracks total processed events
- Shows count after each SET

---

## 🔄 Integration

### With Okta

Configure Okta transmitter stream to send to:
```
https://your-receiver.railway.app/receive-set
```

### Local Testing

1. Start receiver: `./scripts/receiver.sh`
2. Configure Okta to send to: `http://localhost:8081/receive-set`
3. Or use ngrok: `ngrok http 8081`
4. Configure Okta to send to ngrok URL

---

## 📊 Supported Events

All 6 Okta-supported event types:
- DEVICE_RISK_CHANGE
- IP_CHANGE
- USER_RISK_CHANGE
- DEVICE_COMPLIANCE_CHANGE
- SESSION_REVOKED
- IDENTIFIER_CHANGED

Each logs with appropriate icon and formatting!

---

## 🚀 Next Steps

1. **Start receiver:** `./scripts/receiver.sh`
2. **Configure Okta** to send events to receiver
3. **Watch logs** - See formatted events in console
4. **View history** - GET /events to see all received

---

**Receiver is ready to accept SETs from Okta with beautiful formatted logging!** 📨✨
