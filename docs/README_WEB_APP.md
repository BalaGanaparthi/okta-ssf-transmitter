# SSF Transmitter Web Application

A beautiful, modern web interface for sending Security Event Tokens (SETs) to Okta using the Shared Signals Framework (SSF).

## 🎨 Features

- **Stunning UI** - Modern, responsive design with animated background
- **Easy to Use** - Simple form interface for sending security events
- **Event Types** - Dropdown with all supported SSF event types
- **Real-time Feedback** - Instant response display with success/error states
- **JWKS Endpoint** - Automatic public key exposure at `/.well-known/jwks.json`
- **Auto Key Generation** - RSA keys generated automatically on first run
- **Docker Ready** - Containerized for easy deployment
- **Railway Compatible** - Deploy to Railway with one click

## 🚀 Quick Start

### Local Development

1. **Clone and setup**
   ```bash
   git clone <your-repo-url>
   cd project005-SSF
   ```

2. **Run the application**
   ```bash
   ./run.sh
   ```

   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

3. **Access the UI**
   - Open http://localhost:8080 in your browser
   - View JWKS at http://localhost:8080/.well-known/jwks.json

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
ISSUER=https://your-system.example.com
OKTA_DOMAIN=https://your-org.okta.com
KEY_ID=transmitter-key-1
PORT=8080
```

## 🌐 Deploy to Railway

Deploy to Railway in minutes! See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed instructions.

Quick steps:
1. Push code to GitHub
2. Connect to Railway
3. Set environment variables
4. Deploy!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

## 📁 Project Structure

```
project005-SSF/
├── app.py                      # Flask application
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Web UI
├── static/
│   ├── css/
│   │   └── style.css          # Stunning styles
│   └── js/
│       └── app.js             # Frontend logic
├── certs/
│   ├── README.md              # Certificate documentation
│   ├── private_key.pem        # Auto-generated (not in git)
│   └── public_key.pem         # Auto-generated (not in git)
├── RAILWAY_DEPLOYMENT.md      # Railway deployment guide
├── SSF_SETUP_GUIDE.md         # Okta SSF setup guide
└── README.md                   # Original documentation
```

## 🎯 Supported Event Types

### 1. Credential Change Required
Send when user credentials are compromised and need to be changed.

**Use Cases:**
- Password found in data breach
- Credential stuffing detected
- Suspicious account activity

### 2. Account Disabled
Request Okta to disable a user account due to security concerns.

**Use Cases:**
- Multiple failed login attempts
- Malicious activity detected
- Security policy violation

### 3. Account Enabled
Notify Okta that a previously disabled account is now safe.

**Use Cases:**
- Investigation completed
- False positive resolved
- User verified legitimate

## 🔐 Security Features

- **RSA-256 Signatures** - All SETs are cryptographically signed
- **Automatic Key Management** - Keys generated and stored securely
- **JWKS Endpoint** - Public key accessible for verification
- **No Key Exposure** - Private keys never leave the server
- **HTTPS Ready** - Designed for secure production deployment

## 🛠️ API Endpoints

### Web UI
- `GET /` - Main web interface

### API Endpoints
- `GET /api/config` - Get public configuration
- `GET /api/event-types` - Get available event types
- `POST /api/send-event` - Send a security event

### Standard Endpoints
- `GET /.well-known/jwks.json` - JWKS public key endpoint
- `GET /health` - Health check

## 📡 Usage Example

### Via Web UI
1. Enter user email (must exist in Okta)
2. Select event type from dropdown
3. Add optional reason
4. Click "Send Security Event"

### Via API
```bash
curl -X POST http://localhost:8080/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "user@example.com",
    "eventType": "CREDENTIAL_CHANGE_REQUIRED",
    "reason": "Password found in data breach"
  }'
```

### Response
```json
{
  "success": true,
  "status": 202,
  "data": {
    "message": "Event accepted"
  }
}
```

## 🐳 Docker

### Build
```bash
docker build -t ssf-transmitter .
```

### Run
```bash
docker run -p 8080:8080 \
  -e ISSUER=https://your-system.example.com \
  -e OKTA_DOMAIN=https://your-org.okta.com \
  -e KEY_ID=transmitter-key-1 \
  ssf-transmitter
```

## 🔧 Configuration

### Required Environment Variables
- `ISSUER` - Your system's issuer URL (must be publicly accessible)
- `OKTA_DOMAIN` - Your Okta organization URL
- `KEY_ID` - Key identifier for JWKS (default: transmitter-key-1)

### Optional Environment Variables
- `PORT` - Port to run on (default: 8080, Railway sets this automatically)

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
The application logs all events:
- Key generation
- Startup information
- Event transmissions
- Errors and warnings

## 🧪 Testing

1. **Test locally** with the web UI
2. **Verify JWKS** endpoint is accessible
3. **Register provider** in Okta
4. **Send test event** to a test user
5. **Check Okta logs** for event reception

See [SSF_SETUP_GUIDE.md](SSF_SETUP_GUIDE.md) for detailed Okta setup.

## 🐛 Troubleshooting

### Application won't start
- Check Python version (3.11+ recommended)
- Verify all dependencies installed
- Check port 8080 is available

### Keys not generated
- Check file permissions on `certs/` directory
- Verify write access

### Events not reaching Okta
- Verify provider registered in Okta
- Check JWKS URL is publicly accessible
- Ensure user email exists in Okta
- Review Okta system logs

### JWKS endpoint 404
- Verify application is running
- Check route configuration
- Test with: `curl http://localhost:8080/.well-known/jwks.json`

## 📚 Additional Resources

- [Railway Deployment Guide](RAILWAY_DEPLOYMENT.md) - Deploy to Railway
- [SSF Setup Guide](SSF_SETUP_GUIDE.md) - Configure Okta
- [Okta SSF Docs](https://developer.okta.com/docs/guides/configure-ssf-receiver/)
- [OpenID Shared Signals](https://openid.net/wg/sharedsignals/)
- [RFC 8417 - SETs](https://datatracker.ietf.org/doc/html/rfc8417)

## 🎨 UI Preview

The web interface features:
- Animated starfield background
- Gradient card designs
- Smooth transitions and animations
- Responsive layout for mobile/desktop
- Real-time status updates
- Beautiful form controls
- Success/error response displays

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with Flask, Python, and modern web technologies
- Designed for Okta's Shared Signals Framework
- Inspired by modern web design principles

---

**Made with ❤️ for secure identity management**
