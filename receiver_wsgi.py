"""
WSGI Entry Point for SSF Receiver
"""

import os
from src.ssf_receiver.app import create_receiver_app

# Determine environment
env = os.environ.get('FLASK_ENV', 'development')

# Create receiver application
app = create_receiver_app(env)

if __name__ == '__main__':
    # For development only
    port = app.config['RECEIVER_PORT']
    host = app.config['HOST']

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║          SSF Receiver - Receive Events from Okta             ║
╚══════════════════════════════════════════════════════════════╝

🌐 Server starting on {host}:{port}
📨 Receive endpoint: POST /receive-set
📊 View events: GET /events
🔍 Health check: GET /health

Expected Issuer: {app.config['EXPECTED_ISSUER']}

Press Ctrl+C to stop
    """)

    app.run(host=host, port=port, debug=app.config['DEBUG'])
