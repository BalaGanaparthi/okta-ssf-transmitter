# Answer: Deployment Architecture

## Your Questions:

### 1. Will both receiver and transmitter start on same instance in two different ports?
### 2. How to connect to them when deployed on Railway?

---

## ✅ Answer 1: Same Instance, SAME Port

**NO - They run on the SAME port, not different ports.**

### Why?

**Railway limitation:** Railway only exposes **ONE port per service**.

### Solution:

Both transmitter and receiver are combined into a **single Flask application** running on **port 8080** with **different routes**:

```
Single Flask App (Port 8080)
├── Transmitter Routes
│   ├── GET  /                         Web UI
│   ├── POST /api/send-event           Send to Okta
│   └── GET  /.well-known/jwks.json    Public keys
│
└── Receiver Routes
    ├── POST /receive-set               Receive from Okta ⭐
    ├── GET  /receiver/events           View received
    └── POST /receiver/events/clear     Clear history
```

**All accessible via the same domain and port!**

---

## ✅ Answer 2: How to Connect on Railway

### Your Railway URL:
```
https://okta-ssf-transmitter-production-cb28.up.railway.app
```

### Transmitter Access (Send TO Okta):

**Web UI:**
```
https://okta-ssf-transmitter-production-cb28.up.railway.app/
```

**API:**
```
https://okta-ssf-transmitter-production-cb28.up.railway.app/api/send-event
```

**JWKS:**
```
https://okta-ssf-transmitter-production-cb28.up.railway.app/.well-known/jwks.json
```

### Receiver Access (Receive FROM Okta):

**Okta sends to:**
```
https://okta-ssf-transmitter-production-cb28.up.railway.app/receive-set
```

**View received events:**
```
https://okta-ssf-transmitter-production-cb28.up.railway.app/receiver/events
```

**All on the SAME domain!** ✅

---

## 🎯 How It Works

### Deployment Architecture:

```
┌─────────────────────────────────────────────────────────┐
│ Railway Container                                       │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Docker Container                                   │ │
│  │                                                     │ │
│  │  ┌─────────────────────────────────────────────┐  │ │
│  │  │ Gunicorn (WSGI Server)                      │  │ │
│  │  │                                               │  │ │
│  │  │  ┌───────────────────────────────────────┐  │  │ │
│  │  │  │ Flask App (wsgi.py)                   │  │  │ │
│  │  │  │                                         │  │  │ │
│  │  │  │  📤 Transmitter Module                 │  │  │ │
│  │  │  │  ├─ Web UI                             │  │  │ │
│  │  │  │  ├─ API endpoints                      │  │  │ │
│  │  │  │  └─ Okta client                        │  │  │ │
│  │  │  │                                         │  │  │ │
│  │  │  │  📨 Receiver Module                    │  │  │ │
│  │  │  │  ├─ /receive-set endpoint              │  │  │ │
│  │  │  │  ├─ Event processor                    │  │  │ │
│  │  │  │  └─ Console logger                     │  │  │ │
│  │  │  │                                         │  │  │ │
│  │  │  └─────────────────────────────────────────┘  │  │ │
│  │  └───────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  Port 8080 exposed to internet                         │
└─────────────────────────────────────────────────────────┘

Railway URL: https://your-app.railway.app
  ├─ All transmitter routes accessible
  └─ All receiver routes accessible
```

---

## 🔌 Okta Configuration

### For Transmitter (Send TO Okta):

**Register SSF Provider in Okta:**
```
Issuer: https://okta-ssf-transmitter-production-cb28.up.railway.app
JWKS URL: https://okta-ssf-transmitter-production-cb28.up.railway.app/.well-known/jwks.json
```

**Your app sends SETs to:**
```
https://bala-secures-ai.oktapreview.com/security/api/v1/security-events
```

### For Receiver (Receive FROM Okta):

**Configure Okta Stream (if available):**
```
Stream Name: SSF Receiver Stream
Endpoint: https://okta-ssf-transmitter-production-cb28.up.railway.app/receive-set
Method: POST
Content-Type: application/secevent+jwt
```

**Okta will POST SETs to your `/receive-set` endpoint**

---

## 📊 Data Flow

### Bidirectional SSF:

```
Your App (Railway)                    Okta
Port 8080
─────────────────────────────────────────────────────

TRANSMITTING (You → Okta):
Web UI (/api/send-event)
  ↓ Generate & sign JWT
  ↓ POST
  └──────────────────────────→  Okta receives
                                Logs in System Log

RECEIVING (Okta → You):
                                Okta generates SET
                                  ↓ Sign with Okta key
                                  ↓ POST
  /receive-set endpoint  ←──────┘
  ↓ Validate JWT
  ↓ Log formatted output
  └─ Store in memory
  └─ Return 202 Accepted
```

**Both flows work on the same Railway deployment!** ✅

---

## 🧪 Testing After Deployment

### 1. Test Transmitter (Send to Okta):

**Open web UI:**
```
https://okta-ssf-transmitter-production-cb28.up.railway.app/
```

Fill form and send event to Okta.

### 2. Test Receiver (Check received events):

**View events:**
```bash
curl https://okta-ssf-transmitter-production-cb28.up.railway.app/receiver/events | jq
```

**Check Railway logs** for formatted event output when Okta sends.

### 3. Test Receiver Directly (Manual):

```bash
# Send test SET to receiver
curl -X POST https://okta-ssf-transmitter-production-cb28.up.railway.app/receive-set \
  -H "Content-Type: application/secevent+jwt" \
  -d "eyJhbGciOiJSUzI1NiIs..."
```

**Check Railway logs** - see formatted output!

---

## 📋 Summary

### Question 1: Same instance, different ports?
**Answer:** Same instance, **SAME port** (8080), **different routes**

### Question 2: How to connect on Railway?
**Answer:**
- **Same domain:** https://your-app.railway.app
- **Transmitter:** https://your-app.railway.app/ (and /api/*)
- **Receiver:** https://your-app.railway.app/receive-set

### Deployment:
- ✅ Single Docker container
- ✅ Single Railway service
- ✅ Single port (8080)
- ✅ Both transmitter and receiver work
- ✅ No additional configuration

### Okta Setup:
- **For transmitter:** Register provider with JWKS URL
- **For receiver:** Configure stream to POST to /receive-set

---

## 🚀 No Changes Needed!

The current deployment already works:
- ✅ Dockerfile uses wsgi.py
- ✅ wsgi.py now includes both transmitter and receiver
- ✅ Railway exposes port 8080
- ✅ All routes accessible

**Just push and it works!** 🎉

---

## 🎯 Quick Reference

| Component | Port | Routes | Access |
|-----------|------|--------|--------|
| **Transmitter** | 8080 | /, /api/*, /.well-known/* | https://your-app.railway.app/ |
| **Receiver** | 8080 | /receive-set, /receiver/* | https://your-app.railway.app/receive-set |
| **Combined** | 8080 | All routes | Single Railway service ✅ |

---

**Both run on the same port with different routes. No special configuration needed for Railway!** 🚀
