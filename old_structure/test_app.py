#!/usr/bin/env python3
"""
Quick test script to verify the SSF Transmitter application
"""

import subprocess
import time
import requests
import sys
import os

def test_app():
    print("🧪 Testing SSF Transmitter Application\n")

    # Set test environment variables
    os.environ['ISSUER'] = 'https://test.example.com'
    os.environ['OKTA_DOMAIN'] = 'https://test.okta.com'
    os.environ['KEY_ID'] = 'test-key-1'
    os.environ['PORT'] = '8081'

    # Start the Flask app in background
    print("🚀 Starting Flask application...")
    process = subprocess.Popen(
        ['python', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for app to start
    time.sleep(3)

    try:
        base_url = 'http://localhost:8081'

        # Test 1: Health check
        print("✓ Testing health check endpoint...")
        response = requests.get(f'{base_url}/health', timeout=5)
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'
        print("  ✅ Health check passed")

        # Test 2: JWKS endpoint
        print("✓ Testing JWKS endpoint...")
        response = requests.get(f'{base_url}/.well-known/jwks.json', timeout=5)
        assert response.status_code == 200
        jwks = response.json()
        assert 'keys' in jwks
        assert len(jwks['keys']) > 0
        assert jwks['keys'][0]['kid'] == 'test-key-1'
        print("  ✅ JWKS endpoint passed")

        # Test 3: Config endpoint
        print("✓ Testing config endpoint...")
        response = requests.get(f'{base_url}/api/config', timeout=5)
        assert response.status_code == 200
        config = response.json()
        assert config['issuer'] == 'https://test.example.com'
        assert config['oktaDomain'] == 'https://test.okta.com'
        print("  ✅ Config endpoint passed")

        # Test 4: Event types endpoint
        print("✓ Testing event types endpoint...")
        response = requests.get(f'{base_url}/api/event-types', timeout=5)
        assert response.status_code == 200
        event_types = response.json()
        assert 'CREDENTIAL_CHANGE_REQUIRED' in event_types
        assert 'ACCOUNT_DISABLED' in event_types
        assert 'ACCOUNT_ENABLED' in event_types
        print("  ✅ Event types endpoint passed")

        # Test 5: Main page
        print("✓ Testing main page...")
        response = requests.get(base_url, timeout=5)
        assert response.status_code == 200
        assert 'SSF Transmitter' in response.text
        print("  ✅ Main page passed")

        print("\n🎉 All tests passed!")
        print(f"\n📍 Application running at: {base_url}")
        print(f"📍 JWKS endpoint: {base_url}/.well-known/jwks.json")
        return True

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return False

    finally:
        # Stop the Flask app
        print("\n🛑 Stopping application...")
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
        print("✓ Application stopped")

if __name__ == '__main__':
    success = test_app()
    sys.exit(0 if success else 1)
