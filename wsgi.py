"""
WSGI Entry Point - Combined Transmitter + Receiver

Both transmitter and receiver run on the same port:
- Transmitter: /, /api/*, /.well-known/*
- Receiver: /receive-set, /receiver/*
"""

import os
from src.ssf_transmitter.app import create_app
from src.ssf_receiver.core import JWTValidator, EventProcessor
from src.ssf_receiver.api import create_blueprint as create_receiver_blueprint

# Determine environment
env = os.environ.get('FLASK_ENV', 'production')

# Create transmitter application
app = create_app(env)

# Add receiver functionality to the same app
receiver_config = {
    'EXPECTED_ISSUER': os.environ.get('OKTA_DOMAIN', app.config['OKTA_DOMAIN']),
    'OKTA_JWKS_URL': os.environ.get('OKTA_JWKS_URL', f"{app.config['OKTA_DOMAIN']}/.well-known/jwks.json")
}

# Initialize receiver components
jwt_validator = JWTValidator(
    expected_issuer=receiver_config['EXPECTED_ISSUER'],
    jwks_url=receiver_config.get('OKTA_JWKS_URL')
)
event_processor = EventProcessor()

# Register receiver blueprint with /receiver prefix
receiver_bp = create_receiver_blueprint(jwt_validator, event_processor)
app.register_blueprint(receiver_bp, url_prefix='/receiver')

# Add direct /receive-set route (for Okta to POST to)
@app.route('/receive-set', methods=['POST'])
def receive_set():
    """Main receiver endpoint for Okta"""
    from flask import request

    # Use the receiver blueprint's receive_set function
    with app.app_context():
        # Get the view function from the receiver blueprint
        view_func = app.view_functions['receiver.receive_set']
        return view_func()

# Log combined mode
app.logger.info("=" * 80)
app.logger.info("🔄 COMBINED MODE: Transmitter + Receiver on same port")
app.logger.info("=" * 80)
app.logger.info("📤 Transmitter routes:")
app.logger.info("   GET  /                        Web UI")
app.logger.info("   POST /api/send-event          Send to Okta")
app.logger.info("   GET  /.well-known/jwks.json   Public keys")
app.logger.info("")
app.logger.info("📨 Receiver routes:")
app.logger.info("   POST /receive-set             Receive from Okta ⭐")
app.logger.info("   GET  /receiver/events         View received events")
app.logger.info("   POST /receiver/events/clear   Clear history")
app.logger.info("   GET  /receiver/health         Receiver health")
app.logger.info("=" * 80)

if __name__ == '__main__':
    # For development only
    port = app.config['PORT']
    host = app.config['HOST']

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║     Combined SSF Application (Transmitter + Receiver)        ║
╚══════════════════════════════════════════════════════════════╝

🌐 Server: {host}:{port}

📤 TRANSMITTER (Send to Okta):
   Web UI:      http://localhost:{port}/
   Send Event:  POST /api/send-event
   JWKS:        GET /.well-known/jwks.json

📨 RECEIVER (Receive from Okta):
   Receive SET: POST /receive-set ⭐
   View Events: GET /receiver/events
   Clear:       POST /receiver/events/clear

🔑 Keys: {app.config['PRIVATE_KEY_PATH']}
📡 Okta: {app.config['OKTA_DOMAIN']}

Press Ctrl+C to stop
    """)

    app.run(host=host, port=port, debug=app.config['DEBUG'])
