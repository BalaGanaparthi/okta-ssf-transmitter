"""
SSF Transmitter Web Application
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import jwt
import requests
import uuid
import time
import os
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from pathlib import Path

app = Flask(__name__)
CORS(app)

# ============================================================================
# Configuration from Environment Variables
# ============================================================================

ISSUER = os.environ.get('ISSUER', 'https://mysystem.example.com')
OKTA_DOMAIN = os.environ.get('OKTA_DOMAIN', 'https://your-org.okta.com')
KEY_ID = os.environ.get('KEY_ID', 'transmitter-key-1')
CERTS_DIR = Path('./certs')
PRIVATE_KEY_PATH = CERTS_DIR / 'private_key.pem'
PUBLIC_KEY_PATH = CERTS_DIR / 'public_key.pem'

# ============================================================================
# Supported Event Types
# ============================================================================

EVENT_TYPES = {
    'CREDENTIAL_CHANGE_REQUIRED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required',
        'label': 'Credential Change Required',
        'description': 'User credentials are compromised and need to be changed'
    },
    'ACCOUNT_DISABLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-disabled',
        'label': 'Account Disabled',
        'description': 'User account should be disabled due to security concerns'
    },
    'ACCOUNT_ENABLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-enabled',
        'label': 'Account Enabled',
        'description': 'Previously disabled account is now safe to re-enable'
    }
}

# ============================================================================
# Key Management
# ============================================================================

def ensure_keys_exist():
    """Generate RSA key pair if they don't exist"""
    CERTS_DIR.mkdir(exist_ok=True)

    if not PRIVATE_KEY_PATH.exists() or not PUBLIC_KEY_PATH.exists():
        print("🔑 Generating new RSA key pair...")

        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Save private key
        with open(PRIVATE_KEY_PATH, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Get public key
        public_key = private_key.public_key()

        # Save public key
        with open(PUBLIC_KEY_PATH, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        print("✅ Keys generated successfully")
    else:
        print("✅ Keys already exist")

def get_jwks():
    """Generate JWKS from public key"""
    with open(PUBLIC_KEY_PATH, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

    # Get public numbers
    public_numbers = public_key.public_numbers()

    # Convert to base64url encoding
    def int_to_base64url(num):
        num_bytes = num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')
        import base64
        return base64.urlsafe_b64encode(num_bytes).rstrip(b'=').decode('utf-8')

    jwks = {
        "keys": [
            {
                "kty": "RSA",
                "use": "sig",
                "kid": KEY_ID,
                "alg": "RS256",
                "n": int_to_base64url(public_numbers.n),
                "e": int_to_base64url(public_numbers.e)
            }
        ]
    }

    return jwks

# ============================================================================
# SET Generator
# ============================================================================

def generate_set(event_type_uri, subject, reason=None):
    """Generate a Security Event Token (SET)"""
    with open(PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()

    jti = f"evt_{str(uuid.uuid4())}"
    iat = int(time.time())

    payload = {
        'iss': ISSUER,
        'jti': jti,
        'iat': iat,
        'aud': OKTA_DOMAIN,
        'events': {}
    }

    event_data = {
        'subject': {
            'format': 'email',
            'email': subject
        }
    }

    if reason:
        event_data['reason'] = reason

    payload['events'][event_type_uri] = event_data

    headers = {
        'alg': 'RS256',
        'kid': KEY_ID,
        'typ': 'secevent+jwt'
    }

    token = jwt.encode(payload, private_key, algorithm='RS256', headers=headers)
    return token

def send_set(set_token):
    """Send SET to Okta"""
    endpoint = f"{OKTA_DOMAIN}/security/api/v1/security-events"

    try:
        response = requests.post(
            endpoint,
            data=set_token,
            headers={'Content-Type': 'application/secevent+jwt'},
            timeout=10
        )

        response.raise_for_status()

        return {
            'success': True,
            'status': response.status_code,
            'data': response.json() if response.content else None
        }

    except requests.exceptions.HTTPError as e:
        return {
            'success': False,
            'status': e.response.status_code,
            'error': e.response.json() if e.response.content else str(e)
        }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': 'Request failed',
            'details': str(e)
        }

# ============================================================================
# Routes
# ============================================================================

@app.route('/')
def index():
    """Render the main UI"""
    return render_template('index.html')

@app.route('/.well-known/jwks.json')
def jwks():
    """Expose JWKS endpoint"""
    return jsonify(get_jwks())

@app.route('/api/event-types')
def get_event_types():
    """Get available event types"""
    return jsonify(EVENT_TYPES)

@app.route('/api/config')
def get_config():
    """Get public configuration"""
    return jsonify({
        'issuer': ISSUER,
        'oktaDomain': OKTA_DOMAIN,
        'keyId': KEY_ID,
        'jwksUrl': f"{ISSUER}/.well-known/jwks.json"
    })

@app.route('/api/send-event', methods=['POST'])
def send_event():
    """Send a security event"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    subject = data.get('subject')
    event_type = data.get('eventType')
    reason = data.get('reason')

    if not subject or not event_type:
        return jsonify({'error': 'Subject and event type are required'}), 400

    if event_type not in EVENT_TYPES:
        return jsonify({'error': 'Invalid event type'}), 400

    try:
        # Generate SET
        event_uri = EVENT_TYPES[event_type]['uri']
        set_token = generate_set(event_uri, subject, reason)

        # Send to Okta
        result = send_set(set_token)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

# ============================================================================
# Initialization
# ============================================================================

if __name__ == '__main__':
    # Ensure keys exist on startup
    ensure_keys_exist()

    # Get port from environment or default to 8080
    port = int(os.environ.get('PORT', 8080))

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║          SSF Transmitter Web Application                     ║
╚══════════════════════════════════════════════════════════════╝

🌐 Server starting on port {port}
🔑 JWKS endpoint: /.well-known/jwks.json
📡 Issuer: {ISSUER}
🎯 Okta Domain: {OKTA_DOMAIN}
    """)

    app.run(host='0.0.0.0', port=port, debug=False)
