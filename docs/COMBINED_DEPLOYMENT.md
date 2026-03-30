# Combined Transmitter + Receiver Deployment

## Overview

Both transmitter and receiver run **on the same port** in a single Docker container on Railway.

---

## 🎯 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Railway Container (Single Port: 8080)                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Combined Flask Application                           │  │
│  │                                                       │  │
│  │  📤 TRANSMITTER ROUTES:                              │  │
│  │  ├─ GET  /                    (Web UI)               │  │
│  │  ├─ POST /api/send-event      (Send to Okta)        │  │
│  │  └─ GET  /.well-known/jwks.json (Public keys)       │  │
│  │                                                       │  │
│  │  📨 RECEIVER ROUTES:                                 │  │
│  │  ├─ POST /receive-set         (Receive from Okta)   │  │
│  │  ├─ GET  /receiver/events     (View received)       │  │
│  │  ├─ POST /receiver/events/clear (Clear history)     │  │
│  │  └─ GET  /receiver/health     (Health check)        │  │
│  │                                                       │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

Port 8080 exposed to internet via Railway
```

---

## 🌐 URL Structure on Railway

If your Railway URL is: `https://okta-ssf-transmitter-production-cb28.up.railway.app`

### Transmitter Endpoints:
```
https://okta-ssf-transmitter-production-cb28.up.railway.app/
  └─ Web UI for sending events

https://okta-ssf-transmitter-production-cb28.up.railway.app/api/send-event
  └─ API to send events to Okta

https://okta-ssf-transmitter-production-cb28.up.railway.app/.well-known/jwks.json
  └─ Public keys for signature verification
```

### Receiver Endpoints:
```
https://okta-ssf-transmitter-production-cb28.up.railway.app/receive-set ⭐
  └─ Okta sends SETs here

https://okta-ssf-transmitter-production-cb28.up.railway.app/receiver/events
  └─ View received events (GET)

https://okta-ssf-transmitter-production-cb28.up.railway.app/receiver/events/clear
  └─ Clear event history (POST)

https://okta-ssf-transmitter-production-cb28.up.railway.app/receiver/health
  └─ Receiver health check
```

---

## 🚀 Deployment on Railway

### No Changes Needed!

The Dockerfile already uses `wsgi.py` which now includes both transmitter and receiver.

**Railway will:**
1. Build Docker image
2. Start with `CMD ["sh", "scripts/start.sh"]`
3. Gunicorn runs `wsgi:app`
4. Both transmitter and receiver available on port 8080
5. Railway exposes port 8080 to internet

---

## ⚙️ Railway Configuration

### Environment Variables (Same as Before):

```env
ISSUER=https://okta-ssf-transmitter-production-cb28.up.railway.app
OKTA_DOMAIN=https://bala-secures-ai.oktapreview.com
KEY_ID=transmitter-key-1
FLASK_ENV=production
```

**No additional configuration needed!** The receiver uses the same `OKTA_DOMAIN` as expected issuer.

---

## 🔌 Connecting to Receiver from Okta

### In Okta Admin Console:

**Configure SSF Stream (if Okta has transmitter capability):**

**Stream Configuration:**
```
Name: Send to SSF Receiver
Endpoint: https://okta-ssf-transmitter-production-cb28.up.railway.app/receive-set
Content-Type: application/secevent+jwt
Method: POST
```

### Okta Will:
1. Generate SETs for security events
2. Sign with Okta's private key
3. POST to your `/receive-set` endpoint
4. Your receiver logs them in Railway logs

---

## 📊 How to View Received Events

### Option 1: Railway Logs (Recommended)

1. Go to Railway dashboard
2. Click your service
3. Go to "Deployments" → Latest → "View Logs"
4. When Okta sends a SET, you'll see:

```
================================================================================
📨 RECEIVED SET FROM OKTA
================================================================================
🎯 EVENT TYPE: user-risk-change
  👤 User: john@doe.net
  📱 Device: device-001
┌──────────────────────────────────────────────────────────────────────────────┐
│ 👤 User Risk Change                                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│ 🕐 Received: 2024-03-29 19:30:45                                             │
│ 👤 User:     john@doe.net                                                    │
│ 📱 Device:   device-001                                                      │
│ Event Data: current_level = high, previous_level = low                      │
└──────────────────────────────────────────────────────────────────────────────┘
✅ SET PROCESSING COMPLETE
================================================================================
```

### Option 2: API Endpoint

```bash
# View all received events
curl https://okta-ssf-transmitter-production-cb28.up.railway.app/receiver/events | jq

# Clear history
curl -X POST https://okta-ssf-transmitter-production-cb28.up.railway.app/receiver/events/clear
```

---

## 🧪 Testing Locally

### Terminal 1: Start Combined App
```bash
./scripts/dev.sh
# or
python wsgi.py
```

**Runs on port 8080 with BOTH transmitter and receiver**

### Terminal 2: Test Transmitter
```bash
# Open web UI
open http://localhost:8080

# Send event to Okta
curl -X POST http://localhost:8080/api/send-event \
  -H "Content-Type: application/json" \
  -d '{"subject":"test@example.com","eventType":"USER_RISK_CHANGE","device_id":"device-001","current_level":"high","previous_level":"low"}'
```

### Terminal 3: Test Receiver
```bash
# Send test SET to receiver
curl -X POST http://localhost:8080/receive-set \
  -H "Content-Type: application/secevent+jwt" \
  -d "eyJhbGciOiJSUzI1NiIs..."

# View received events
curl http://localhost:8080/receiver/events | jq
```

**Watch Terminal 1** - See formatted logs for received SETs!

---

## 📋 Route Summary

| Route | Component | Purpose |
|-------|-----------|---------|
| `/` | Transmitter | Web UI |
| `/api/send-event` | Transmitter | Send to Okta |
| `/api/event-types` | Transmitter | Event types |
| `/api/verify-keys` | Transmitter | Key verification |
| `/api/debug-event` | Transmitter | Debug JWT |
| `/.well-known/jwks.json` | Transmitter | Public keys |
| `/health` | Transmitter | Health check |
| **`/receive-set`** | **Receiver** | **Receive from Okta** ⭐ |
| `/receiver/events` | Receiver | View received |
| `/receiver/events/clear` | Receiver | Clear history |
| `/receiver/health` | Receiver | Receiver health |

---

## 🔍 Benefits of Combined Deployment

### 1. **Single Port** ✅
- Railway only exposes one port per service
- Both transmitter and receiver accessible

### 2. **Shared Configuration** ✅
- Same environment variables
- Same Okta domain
- Same keys

### 3. **Unified Logging** ✅
- All logs in one place (Railway logs)
- Easy to see both transmissions and receptions

### 4. **Simple Deployment** ✅
- One Docker container
- One Railway service
- One domain

---

## 💡 How This Works

### When You Send Event (Transmitter):
```
Your Browser
  → POST /api/send-event (Port 8080)
  → Transmitter generates JWT
  → Transmitter POSTs to Okta
  → Response shown in UI
```

### When Okta Sends Event (Receiver):
```
Okta
  → POST /receive-set (Port 8080)
  → Receiver validates JWT
  → Receiver logs to console (formatted)
  → Returns 202 Accepted
  → Event stored in memory
```

**Both happen on the same server, same port!** ✅

---

## 🎯 Configuration for Okta

### In Your Okta Org:

**1. Register SSF Provider (for transmitter):**
```
Issuer: https://okta-ssf-transmitter-production-cb28.up.railway.app
JWKS URL: https://okta-ssf-transmitter-production-cb28.up.railway.app/.well-known/jwks.json
```

**2. Configure SSF Stream (for receiver):**
```
Stream Endpoint: https://okta-ssf-transmitter-production-cb28.up.railway.app/receive-set
Method: POST
Content-Type: application/secevent+jwt
```

---

## 🧪 Testing End-to-End Flow

### Scenario: Round-trip SSF Test

**1. Start app locally:**
```bash
python wsgi.py
```

**2. Use transmitter to generate SET:**
```bash
JWT=$(curl -s -X POST http://localhost:8080/api/debug-event \
  -H "Content-Type: application/json" \
  -d '{"subject":"test@example.com","eventType":"USER_RISK_CHANGE","device_id":"device-001","current_level":"high","previous_level":"low"}' \
  | jq -r '.jwt_token')
```

**3. Send to receiver:**
```bash
curl -X POST http://localhost:8080/receive-set \
  -H "Content-Type: application/secevent+jwt" \
  -d "$JWT"
```

**4. Check logs:**
You'll see formatted output in the console! 📨

**5. View history:**
```bash
curl http://localhost:8080/receiver/events | jq
```

---

## 📊 Railway Logs

### When Receiving SETs from Okta:

Railway logs will show:
```
[INFO] ================================================================================
[INFO] 📨 RECEIVED SET FROM OKTA
[INFO] ================================================================================
[INFO] 🎯 EVENT TYPE: user-risk-change
[INFO]   👤 User: john@doe.net
[INFO]   📱 Device: device-001
[INFO]   current_level: high
[INFO]   previous_level: low
[INFO] ┌──────────────────────────────────────────────────────────────────────────────┐
[INFO] │ 👤 User Risk Change                                                          │
[INFO] └──────────────────────────────────────────────────────────────────────────────┘
[INFO] ✅ SET PROCESSING COMPLETE
```

Beautiful formatted logs visible in Railway dashboard!

---

## 🎉 Summary

**Question:** Will both run on same instance in different ports?

**Answer:** Both run on **SAME port** (8080) with **different routes**:
- Transmitter: `/`, `/api/*`, `/.well-known/*`
- Receiver: `/receive-set`, `/receiver/*`

**Railway Deployment:**
- ✅ Single Docker container
- ✅ Single port (8080)
- ✅ Both transmitter and receiver accessible
- ✅ Unified logging in Railway

**Okta Connection:**
- **Send TO Okta:** Your app uses `/api/send-event` → POSTs to Okta
- **Receive FROM Okta:** Okta POSTs to your `/receive-set` endpoint

**No additional configuration needed!** Push and it works! 🚀

---

## 🚀 Push Command

```bash
git push origin main
```

**After deploying:**
- Transmitter: https://your-app.railway.app/ (Web UI)
- Receiver: https://your-app.railway.app/receive-set (Okta POSTs here)
- View events: https://your-app.railway.app/receiver/events

**Both on same domain, same port!** ✅
