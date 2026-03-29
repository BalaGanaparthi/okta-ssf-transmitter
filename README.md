# SSF Transmitter

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/tests-24%2F24%20passing-success.svg)]()

A production-grade web application for transmitting Security Event Tokens (SETs) to Okta using the Shared Signals Framework (SSF).

## 🌟 Features

- **Modern Web UI** - Beautiful interface with dynamic form generation
- **6 Supported Event Types** - Only events Okta officially supports
- **Dynamic Forms** - UI automatically adapts to each event type
- **Smart Dropdowns** - Enum values pre-populated (risk levels, compliance status, IP addresses)
- **JWT Visibility** - See complete JWT token, header, and payload
- **JWT.io Integration** - One-click token inspection
- **DateTime Conversion** - Automatic Unix timestamp conversion
- **JWKS Endpoint** - Public key at `/.well-known/jwks.json`
- **Docker Ready** - Containerized for Railway deployment
- **Enhanced Logging** - Detailed transmission logs with timestamps

## 🚀 Quick Start

### Local Development

```bash
# Run development server
./scripts/dev.sh

# Or using Make
make run-dev

# Access the application
open http://localhost:8080
```

### Deploy to Railway

```bash
# Push to GitHub
git push origin main

# Railway auto-deploys using Dockerfile
# Set environment variables in Railway dashboard:
#   ISSUER=https://your-app.railway.app
#   OKTA_DOMAIN=https://your-org.okta.com
#   KEY_ID=transmitter-key-1
```

See [docs/COMPLETE_SETUP_GUIDE.md](docs/COMPLETE_SETUP_GUIDE.md) for detailed steps.

## ⚙️ Configuration

Create `.env` file:

```bash
cp .env.example .env
```

Edit with your values:
```env
ISSUER=https://your-app.railway.app
OKTA_DOMAIN=https://your-org.okta.com
KEY_ID=transmitter-key-1
PORT=8080
FLASK_ENV=production
```

## 🎯 Supported Event Types (6 Total)

### Okta Events (3)
- **Device Risk Change** - Device risk level changes with current/previous levels
- **IP Change** - User IP address changes with current/previous IPs
- **User Risk Change** - User risk level changes with current/previous levels

### CAEP Events (2)
- **Device Compliance Change** - Device compliance status changes
- **Session Revoked** - User session revocation with optional session ID

### RISC Events (1)
- **Identifier Changed** - User identifier (email/phone) modification

## 🔌 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Web UI |
| `/.well-known/jwks.json` | JWKS public keys |
| `/api/event-types` | Event types with field schemas |
| `/api/send-event` | Send security event |
| `/api/verify-keys` | Verify loaded keys |
| `/health` | Health check |

## 🧪 Testing

```bash
make test              # Run all tests
make coverage          # Run with coverage
pytest tests/ -v       # Verbose output
```

All 24 tests passing ✅

## 🐳 Docker

```bash
docker build -t ssf-transmitter .
docker run -p 8080:8080 \
  -e ISSUER=https://your-app.railway.app \
  -e OKTA_DOMAIN=https://your-org.okta.com \
  ssf-transmitter
```

## 📚 Documentation

Complete guides in [docs/](docs/):
- [Complete Setup Guide](docs/COMPLETE_SETUP_GUIDE.md) - End-to-end setup
- [Railway Deployment](docs/RAILWAY_DEPLOYMENT.md) - Deploy to Railway
- [Event Types Guide](docs/SSF_EVENT_TYPES_GUIDE.md) - All 15 event types
- [Architecture](docs/ARCHITECTURE.md) - System design

## 🔐 Security

- RSA-256 JWT signatures
- Private keys secured in certs/ folder
- Environment-based configuration
- No hardcoded secrets
- HTTPS ready

## 📞 Support

- Documentation: [docs/](docs/)
- Okta Docs: [developer.okta.com](https://developer.okta.com/)

---

**Built for Okta Identity Threat Protection with Shared Signals Framework**
