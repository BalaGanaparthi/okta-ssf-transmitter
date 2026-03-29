# SSF Transmitter

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A production-grade web application for transmitting Security Event Tokens (SETs) to Okta using the Shared Signals Framework (SSF).

## 🌟 Features

- **Modern Web UI** - Beautiful, responsive interface with real-time feedback
- **SSF Compliant** - Fully implements OpenID Shared Signals Framework
- **Auto Key Management** - Automatic RSA key generation and rotation
- **JWKS Endpoint** - Public key exposure at `/.well-known/jwks.json`
- **Docker Ready** - Containerized for easy deployment
- **Railway Compatible** - Deploy to Railway with one click
- **Production Ready** - Gunicorn, logging, health checks, and monitoring
- **Comprehensive Tests** - Full test suite with pytest

## 📁 Project Structure

```
ssf-transmitter/
├── src/
│   └── ssf_transmitter/          # Main application package
│       ├── api/                  # API routes and endpoints
│       ├── core/                 # Business logic
│       │   ├── event_types.py   # SSF event type definitions
│       │   ├── jwt_handler.py   # JWT/SET generation
│       │   └── key_manager.py   # RSA key management
│       ├── services/             # External service integrations
│       │   └── okta_client.py   # Okta API client
│       ├── utils/                # Utility functions
│       ├── templates/            # HTML templates
│       ├── static/               # CSS, JS, images
│       ├── app.py               # Flask app factory
│       └── config.py            # Configuration management
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest fixtures
│   ├── test_api.py              # API tests
│   └── test_core.py             # Core module tests
├── scripts/                      # Utility scripts
│   ├── dev.sh                   # Development server
│   └── start.sh                 # Production server (Gunicorn)
├── docs/                         # Documentation
├── certs/                        # Certificate storage (auto-generated)
├── wsgi.py                       # WSGI entry point
├── Dockerfile                    # Docker configuration
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
├── Makefile                      # Build automation
└── setup.py                      # Package configuration
```

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/ssf-transmitter.git
cd ssf-transmitter

# Run development server
make run-dev
# or
./scripts/dev.sh

# Access the application
open http://localhost:8080
```

### Using Docker

```bash
# Build image
make docker-build

# Run container
make docker-run
```

### Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

See [docs/RAILWAY_DEPLOYMENT.md](docs/RAILWAY_DEPLOYMENT.md) for detailed instructions.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
# Your system's issuer URL
ISSUER=https://your-app.railway.app

# Okta domain
OKTA_DOMAIN=https://your-org.okta.com

# Key ID for JWKS
KEY_ID=transmitter-key-1

# Server port (Railway sets this automatically)
PORT=8080

# Flask environment
FLASK_ENV=production
```

### Application Configuration

The application uses a configuration class system:
- `DevelopmentConfig` - Local development with debug mode
- `ProductionConfig` - Production deployment
- `TestingConfig` - Test suite execution

See `src/ssf_transmitter/config.py` for details.

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage report
make coverage

# Run specific test file
pytest tests/test_api.py -v
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md) - Get started in minutes
- [Railway Deployment](docs/RAILWAY_DEPLOYMENT.md) - Deploy to Railway
- [Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md) - Production deployment guide
- [API Documentation](docs/README_WEB_APP.md) - API endpoints and usage
- [Okta Setup](docs/SSF_SETUP_GUIDE.md) - Configure Okta SSF receiver

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI |
| `/.well-known/jwks.json` | GET | JWKS public keys |
| `/api/config` | GET | Public configuration |
| `/api/event-types` | GET | Available event types |
| `/api/send-event` | POST | Send security event |
| `/health` | GET | Health check |

## 🎯 Supported Event Types

- **Credential Change Required** - User credentials compromised
- **Account Disabled** - Account should be suspended
- **Account Enabled** - Account is safe to re-enable

## 🛠️ Development

### Setup Development Environment

```bash
# Install dependencies
make dev

# Run tests
make test

# Format code
make format

# Lint code
make lint
```

### Project Commands

```bash
make help              # Show all available commands
make install           # Install production dependencies
make dev              # Install development dependencies
make test             # Run tests
make coverage         # Run tests with coverage
make lint             # Run linters
make format           # Format code
make clean            # Clean generated files
make docker-build     # Build Docker image
make docker-run       # Run Docker container
make run-dev          # Start development server
make run-prod         # Start production server
```

## 🔐 Security

- **RSA-256 Signatures** - Industry-standard JWT signing
- **Automatic Key Generation** - No manual key management
- **Private Key Protection** - Keys never exposed via API
- **HTTPS Ready** - SSL termination at deployment
- **Environment Variables** - No hardcoded secrets
- **CORS Configuration** - Secure cross-origin requests

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:8080/health
```

### JWKS Verification

```bash
curl http://localhost:8080/.well-known/jwks.json | jq
```

### Logs

Application logs include:
- Startup configuration
- Event transmissions
- Errors and warnings
- Request/response details

## 🐳 Docker

### Build

```bash
docker build -t ssf-transmitter:latest .
```

### Run

```bash
docker run -p 8080:8080 \
  -e ISSUER=https://your-system.com \
  -e OKTA_DOMAIN=https://your-org.okta.com \
  -e KEY_ID=transmitter-key-1 \
  ssf-transmitter:latest
```

## 🚢 Deployment

### Railway

1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

See [docs/RAILWAY_DEPLOYMENT.md](docs/RAILWAY_DEPLOYMENT.md)

### Other Platforms

The application is compatible with:
- Heroku
- AWS ECS/EKS
- Google Cloud Run
- Azure App Service
- Any platform supporting Docker

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Flask and modern web technologies
- Implements OpenID Shared Signals Framework
- Designed for Okta Identity Threat Protection

## 📞 Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/yourusername/ssf-transmitter/issues)
- Okta Support: [Okta Developer Docs](https://developer.okta.com/)

---

**Built with ❤️ for secure identity management**
