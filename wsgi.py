"""
WSGI Entry Point
"""

import os
from src.ssf_transmitter.app import create_app

# Determine environment
env = os.environ.get('FLASK_ENV', 'production')

# Create application
app = create_app(env)

if __name__ == '__main__':
    # For development only
    port = app.config['PORT']
    host = app.config['HOST']

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║          SSF Transmitter Web Application                     ║
╚══════════════════════════════════════════════════════════════╝

🌐 Server starting on {host}:{port}
🔑 JWKS endpoint: /.well-known/jwks.json
📡 Issuer: {app.config['ISSUER']}
🎯 Okta Domain: {app.config['OKTA_DOMAIN']}

Press Ctrl+C to stop
    """)

    app.run(host=host, port=port, debug=app.config['DEBUG'])
