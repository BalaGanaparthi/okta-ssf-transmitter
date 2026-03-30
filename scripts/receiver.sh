#!/bin/bash
# Start SSF Receiver

set -e

echo "🔧 Starting SSF Receiver (Development Mode)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Using defaults..."
fi

# Set development environment
export FLASK_ENV=development
export PYTHONPATH=$PWD

# Start the receiver
echo "🌐 Starting SSF Receiver..."
echo "   Receive endpoint: http://localhost:8081/receive-set"
echo "   View events: http://localhost:8081/events"
echo "   Health check: http://localhost:8081/health"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python receiver_wsgi.py
