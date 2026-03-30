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
                        # Convert datetime-local to Unix timestamp if needed
                        if field_def.get('convert_to') == 'unix_timestamp':
                            try:
                                from datetime import datetime
                                # Parse datetime string (format: "2024-03-29T10:30")
                                dt = datetime.fromisoformat(field_value)
                                # Convert to Unix timestamp
                                field_value = int(dt.timestamp())
                                logger.info(f"Converted {field_name} to Unix timestamp: {field_value}")
                            except Exception as e:
                                logger.error(f"Failed to convert {field_name} to timestamp: {e}")
                                return jsonify({
                                    'error': f"Invalid datetime format for {field_def.get('label', field_name)}"
                                }), 400

                        extra_fields[field_name] = field_value

            # Extract device_id (required by Okta for all events)
            device_id = extra_fields.pop('device_id', None)

            # Convert ALL reason fields to language objects (Okta requires this format)
            if 'reason_admin' in extra_fields and isinstance(extra_fields['reason_admin'], str):
                extra_fields['reason_admin'] = {'en': extra_fields['reason_admin']}
            if 'reason_user' in extra_fields and isinstance(extra_fields['reason_user'], str):
                extra_fields['reason_user'] = {'en': extra_fields['reason_user']}

            # NOTE: Do NOT use general_reason for Okta events
            # Okta events use reason_admin and reason_user as language objects

            # Generate SET with proper Okta structure
            event_uri = get_event_uri(event_type)
            set_token = bp.jwt_handler.generate_set(
                event_uri,
                subject,
                device_id,  # Pass device_id (required)
                None,  # Don't use general reason
                extra_fields if extra_fields else None
            )

            # Decode JWT for display (without verification)
            import jwt as pyjwt
            decoded_payload = pyjwt.decode(set_token, options={"verify_signature": False})
            decoded_header = pyjwt.get_unverified_header(set_token)

            # Send to Okta
            config = current_app.config
            okta_client = OktaClient(config['OKTA_DOMAIN'])
            result = okta_client.send_set(set_token)

            # Add JWT details to response for UI display
            result['jwt_token'] = set_token
            result['jwt_header'] = decoded_header
            result['jwt_payload'] = decoded_payload
            result['okta_endpoint'] = okta_client.endpoint

            # Add info about collected fields for debugging
            result['collected_fields'] = {
                'subject': subject,
                'event_type': event_type,
                'extra_fields': extra_fields,
                'general_reason': general_reason
            }

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

    @bp.route('/api/debug-event', methods=['POST'])
    def debug_event():
        """Debug endpoint - shows what JWT would be generated (doesn't send to Okta)"""
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        subject = data.get('subject')
        event_type = data.get('eventType')

        if not subject or not event_type:
            return jsonify({'error': 'Subject and event type are required'}), 400

        if not validate_event_type(event_type):
            return jsonify({'error': 'Invalid event type'}), 400

        try:
            # Log what we received
            logger.info(f"Debug - Received data: {data}")

            # Dynamically collect extra fields
            from ..core import get_event_type_with_schemas

            extra_fields = {}
            general_reason = None
            event_type_schema = get_event_type_with_schemas(event_type)

            if event_type_schema and event_type_schema.get('field_definitions'):
                for field_def in event_type_schema['field_definitions']:
                    field_name = field_def['name']
                    field_value = data.get(field_name)

                    logger.info(f"Debug - Field {field_name}: {field_value}")

                    if field_value:
                        extra_fields[field_name] = field_value

            if 'reason' not in extra_fields:
                general_reason = data.get('reason')

            logger.info(f"Debug - Extra fields: {extra_fields}")
            logger.info(f"Debug - General reason: {general_reason}")

            # Generate SET
            event_uri = get_event_uri(event_type)
            set_token = bp.jwt_handler.generate_set(
                event_uri,
                subject,
                general_reason,
                extra_fields if extra_fields else None
            )

            # Decode to show payload
            import jwt
            decoded = jwt.decode(set_token, options={"verify_signature": False})

            return jsonify({
                'status': 'debug',
                'received_data': data,
                'extra_fields_collected': extra_fields,
                'general_reason': general_reason,
                'jwt_payload': decoded,
                'message': 'JWT generated successfully (not sent to Okta)'
            })

        except Exception as e:
            logger.error(f"Debug error: {str(e)}", exc_info=True)
            return jsonify({
                'status': 'error',
                'error': str(e)
            }), 500

    return bp
