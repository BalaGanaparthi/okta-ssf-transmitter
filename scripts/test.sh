#!/bin/bash
# Quick test script for production structure

set -e

echo "🧪 Testing SSF Transmitter Production Structure"
echo ""

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "📦 Using existing virtual environment"
    source venv/bin/activate
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
fi

echo "✓ Running tests..."
export PYTHONPATH=$PWD
pytest -v

echo ""
echo "🎉 All tests passed!"
