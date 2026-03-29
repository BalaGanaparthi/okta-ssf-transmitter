"""
Pytest configuration and fixtures
"""

import pytest
from src.ssf_transmitter.app import create_app
from src.ssf_transmitter.core import KeyManager, JWTHandler
from pathlib import Path
import tempfile
import os


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def temp_keys():
    """Create temporary key files for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        private_key_path = Path(tmpdir) / 'private_key.pem'
        public_key_path = Path(tmpdir) / 'public_key.pem'

        key_manager = KeyManager(private_key_path, public_key_path)

        # For testing, we need to generate keys
        # Call the private method directly
        key_manager._generate_keys()

        yield key_manager

        # Cleanup happens automatically


@pytest.fixture
def jwt_handler(temp_keys):
    """Create JWT handler with temporary keys"""
    return JWTHandler(
        key_manager=temp_keys,
        issuer='https://test.example.com',
        audience='https://test.okta.com',
        key_id='test-key-1'
    )
