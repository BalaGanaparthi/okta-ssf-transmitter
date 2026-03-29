#!/bin/bash
# Production start script using Gunicorn

set -e

echo "🚀 Starting SSF Transmitter (Production Mode)"

# Set production environment
export FLASK_ENV=production

# Use gunicorn for production
exec gunicorn \
    --bind 0.0.0.0:${PORT:-8080} \
    --workers ${WORKERS:-4} \
    --timeout ${TIMEOUT:-30} \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    "wsgi:app"
