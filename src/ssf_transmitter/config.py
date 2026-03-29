"""
Application Configuration
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application settings
class Config:
    """Base configuration"""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False

    # SSF Configuration
    ISSUER = os.environ.get('ISSUER', 'https://mysystem.example.com')
    OKTA_DOMAIN = os.environ.get('OKTA_DOMAIN', 'https://your-org.okta.com')
    KEY_ID = os.environ.get('KEY_ID', 'transmitter-key-1')

    # Paths
    CERTS_DIR = BASE_DIR / 'certs'
    PRIVATE_KEY_PATH = CERTS_DIR / 'private_key.pem'
    PUBLIC_KEY_PATH = CERTS_DIR / 'public_key.pem'

    # Server settings
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 8080))

    # Security
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    @property
    def okta_set_endpoint(self):
        """Okta SET endpoint URL"""
        return f"{self.OKTA_DOMAIN}/security/api/v1/security-events"

    @property
    def jwks_url(self):
        """JWKS URL"""
        return f"{self.ISSUER}/.well-known/jwks.json"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    ISSUER = 'https://test.example.com'
    OKTA_DOMAIN = 'https://test.okta.com'


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
