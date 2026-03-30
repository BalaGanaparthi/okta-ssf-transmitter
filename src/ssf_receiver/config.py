"""
SSF Receiver Configuration
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ReceiverConfig:
    """Base receiver configuration"""

    # Flask settings
    SECRET_KEY = os.environ.get('RECEIVER_SECRET_KEY', 'receiver-dev-secret-key')
    DEBUG = False
    TESTING = False

    # Receiver settings
    RECEIVER_PORT = int(os.environ.get('RECEIVER_PORT', 8081))
    HOST = '0.0.0.0'

    # Okta transmitter JWKS URL (to verify signatures from Okta)
    OKTA_JWKS_URL = os.environ.get('OKTA_JWKS_URL', 'https://your-org.okta.com/.well-known/jwks.json')

    # Expected issuer (Okta domain)
    EXPECTED_ISSUER = os.environ.get('EXPECTED_ISSUER', 'https://your-org.okta.com')

    # This receiver's identifier
    RECEIVER_ID = os.environ.get('RECEIVER_ID', 'ssf-receiver-001')


class DevelopmentConfig(ReceiverConfig):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(ReceiverConfig):
    """Production configuration"""
    DEBUG = False


class TestingConfig(ReceiverConfig):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
