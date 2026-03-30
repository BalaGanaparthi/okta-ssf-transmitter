"""
SSF Receiver Flask Application Factory
"""

from flask import Flask
from .config import get_config
from .core import JWTValidator, EventProcessor
from .api import create_blueprint
import logging


def create_receiver_app(config_name=None):
    """
    Create SSF Receiver application

    Args:
        config_name: Configuration name ('development', 'production', 'testing')

    Returns:
        Flask app instance
    """
    app = Flask(__name__)

    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Setup logging
    setup_logging(app)

    # Initialize components
    jwt_validator = JWTValidator(
        expected_issuer=app.config['EXPECTED_ISSUER'],
        jwks_url=app.config.get('OKTA_JWKS_URL')
    )

    event_processor = EventProcessor()

    # Register blueprints
    bp = create_blueprint(jwt_validator, event_processor)
    app.register_blueprint(bp)

    # Log startup info
    app.logger.info("=" * 80)
    app.logger.info("📨 SSF RECEIVER STARTED")
    app.logger.info("=" * 80)
    app.logger.info(f"Environment: {config_name or 'development'}")
    app.logger.info(f"Expected Issuer: {app.config['EXPECTED_ISSUER']}")
    app.logger.info(f"Receiver Endpoint: /receive-set")
    app.logger.info(f"Port: {app.config['RECEIVER_PORT']}")
    app.logger.info("=" * 80)

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
