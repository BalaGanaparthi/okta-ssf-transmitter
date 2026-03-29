#!/bin/bash
# Development start script

set -e

echo "🔧 Starting SSF Transmitter (Development Mode)"

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
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "✏️  Please edit .env with your configuration"
fi

# Set development environment
export FLASK_ENV=development

# Start the application
echo "🌐 Starting Flask application..."
echo "   Access at: http://localhost:8080"
echo "   JWKS at: http://localhost:8080/.well-known/jwks.json"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python wsgi.py
