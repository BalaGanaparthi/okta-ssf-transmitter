"""
API Routes
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from ..core import EVENT_TYPES, get_event_uri, validate_event_type
from ..services.okta_client import OktaClient
import logging

logger = logging.getLogger(__name__)


def create_blueprint(jwt_handler, key_manager):
    """
    Create Flask blueprint with routes

    Args:
        jwt_handler: JWTHandler instance
        key_manager: KeyManager instance

    Returns:
        Flask Blueprint
    """
    bp = Blueprint('ssf', __name__)

    # Store dependencies on blueprint
    bp.jwt_handler = jwt_handler
    bp.key_manager = key_manager

    @bp.route('/')
    def index():
        """Render the main UI"""
        return render_template('index.html')

    @bp.route('/.well-known/jwks.json')
    def jwks():
        """Expose JWKS endpoint"""
        config = current_app.config
        jwks_data = bp.key_manager.get_jwks(config['KEY_ID'])
        return jsonify(jwks_data)

    @bp.route('/api/event-types')
    def get_event_types():
        """Get available event types with field schemas"""
        from ..core import get_event_type_with_schemas, FIELD_SCHEMAS

        # Return event types with resolved field schemas for dynamic UI
        result = {}
        for key in EVENT_TYPES.keys():
            result[key] = get_event_type_with_schemas(key)

        return jsonify(result)

    @bp.route('/api/config')
    def get_config():
        """Get public configuration"""
        config = current_app.config
        jwks_url = f"{config['ISSUER']}/.well-known/jwks.json"
        return jsonify({
            'issuer': config['ISSUER'],
            'oktaDomain': config['OKTA_DOMAIN'],
            'keyId': config['KEY_ID'],
            'jwksUrl': jwks_url
        })

    @bp.route('/api/send-event', methods=['POST'])
    def send_event():
        """Send a security event"""
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        subject = data.get('subject')
        event_type = data.get('eventType')

        # Validation
        if not subject or not event_type:
            return jsonify({'error': 'Subject and event type are required'}), 400

        if not validate_event_type(event_type):
            return jsonify({'error': 'Invalid event type'}), 400

        try:
            # Dynamically collect extra fields based on event type schema
            from ..core import get_event_type_with_schemas

            extra_fields = {}
            general_reason = None
            event_type_schema = get_event_type_with_schemas(event_type)

            if event_type_schema and event_type_schema.get('field_definitions'):
                for field_def in event_type_schema['field_definitions']:
                    field_name = field_def['name']
                    field_value = data.get(field_name)

                    # Check required fields
                    if field_def.get('required', False) and not field_value:
                        return jsonify({
                            'error': f"{field_def.get('label', field_name)} is required for {event_type} event"
                        }), 400

                    # Add to extra_fields if has value
                    if field_value:
                        extra_fields[field_name] = field_value

            # Check for general reason field (from textarea)
            if 'reason' not in extra_fields:
                general_reason = data.get('reason')

            # Generate SET
            event_uri = get_event_uri(event_type)
            set_token = bp.jwt_handler.generate_set(
                event_uri,
                subject,
                general_reason,
                extra_fields if extra_fields else None
            )

            # Send to Okta
            config = current_app.config
            okta_client = OktaClient(config['OKTA_DOMAIN'])
            result = okta_client.send_set(set_token)

            logger.info(f"Event sent: {event_type} for {subject} with fields: {list(extra_fields.keys())}")
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error sending event: {str(e)}", exc_info=True)
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @bp.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy'})

    @bp.route('/api/verify-keys')
    def verify_keys():
        """Verify which keys are being used (for debugging)"""
        try:
            import hashlib

            # Get public key
            public_key = bp.key_manager.get_public_key()

            # Get public key bytes
            from cryptography.hazmat.primitives import serialization
            public_key_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # Calculate fingerprint (SHA256 of public key)
            fingerprint = hashlib.sha256(public_key_bytes).hexdigest()

            # Get JWKS
            config = current_app.config
            jwks = bp.key_manager.get_jwks(config['KEY_ID'])

            return jsonify({
                'status': 'success',
                'key_id': config['KEY_ID'],
                'public_key_fingerprint': fingerprint,
                'public_key_sha256_short': fingerprint[:16] + '...',
                'jwks_kid': jwks['keys'][0]['kid'],
                'jwks_n_length': len(jwks['keys'][0]['n']),
                'message': 'Keys are loaded and valid',
                'note': 'Compare this fingerprint with Okta registration to verify keys match'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e)
            }), 500

    return bp
