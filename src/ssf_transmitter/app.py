"""
Flask Application Factory
"""

from flask import Flask
from flask_cors import CORS
from .config import get_config
from .core import KeyManager, JWTHandler
from .api import create_blueprint
import logging


def create_app(config_name=None):
    """
    Application factory

    Args:
        config_name: Configuration name ('development', 'production', 'testing')

    Returns:
        Flask app instance
    """
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Setup logging
    setup_logging(app)

    # Setup CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    # Initialize key manager
    key_manager = KeyManager(
        app.config['PRIVATE_KEY_PATH'],
        app.config['PUBLIC_KEY_PATH']
    )
    key_manager.ensure_keys_exist()

    # Initialize JWT handler
    jwt_handler = JWTHandler(
        key_manager=key_manager,
        issuer=app.config['ISSUER'],
        audience=app.config['OKTA_DOMAIN'],
        key_id=app.config['KEY_ID']
    )

    # Register blueprints
    bp = create_blueprint(jwt_handler, key_manager)
    app.register_blueprint(bp)

    # Log startup info
    app.logger.info("=" * 70)
    app.logger.info("SSF Transmitter Application Started")
    app.logger.info("=" * 70)
    app.logger.info(f"Environment: {config_name or 'development'}")
    app.logger.info(f"Issuer: {app.config['ISSUER']}")
    app.logger.info(f"Okta Domain: {app.config['OKTA_DOMAIN']}")
    app.logger.info(f"Key ID: {app.config['KEY_ID']}")
    app.logger.info(f"JWKS URL: {app.config['ISSUER']}/.well-known/jwks.json")
    app.logger.info("=" * 70)

    return app


def setup_logging(app):
    """Setup application logging"""
    log_level = logging.DEBUG if app.config['DEBUG'] else logging.INFO

    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Configure app logger
    app.logger.setLevel(log_level)
    app.logger.addHandler(console_handler)

    # Configure root logger
    logging.getLogger().setLevel(log_level)
    logging.getLogger().addHandler(console_handler)
