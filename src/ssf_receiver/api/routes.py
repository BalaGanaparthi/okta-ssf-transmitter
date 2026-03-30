"""
SSF Receiver API Routes
"""

from flask import Blueprint, request, jsonify, render_template
import logging

logger = logging.getLogger(__name__)


def create_blueprint(jwt_validator, event_processor):
    """
    Create Flask blueprint for receiver endpoints

    Args:
        jwt_validator: JWTValidator instance
        event_processor: EventProcessor instance

    Returns:
        Flask Blueprint
    """
    bp = Blueprint('receiver', __name__)

    # Store dependencies on blueprint
    bp.jwt_validator = jwt_validator
    bp.event_processor = event_processor

    @bp.route('/')
    def index():
        """Receiver status page"""
        return jsonify({
            'status': 'operational',
            'service': 'SSF Receiver',
            'version': '1.0.0',
            'endpoint': '/receive-set',
            'processed_events': bp.event_processor.processed_count
        })

    @bp.route('/receive-set', methods=['POST'])
    def receive_set():
        """
        Receive Security Event Token from Okta

        This endpoint receives SETs sent by Okta transmitter.
        Content-Type should be: application/secevent+jwt
        """
        try:
            # Get raw JWT from request body
            set_token = request.get_data(as_text=True)

            if not set_token:
                logger.error("❌ Received empty request")
                return jsonify({'err': 'invalid_request', 'description': 'No SET provided'}), 400

            # Check Content-Type
            content_type = request.headers.get('Content-Type', '')
            logger.info(f"📨 Received SET (Content-Type: {content_type})")

            # Validate and decode JWT
            try:
                header = bp.jwt_validator.get_header(set_token)
                payload = bp.jwt_validator.validate_and_decode(set_token)

                # Process the SET
                result = bp.event_processor.process_set(header, payload, set_token)

                # Return 202 Accepted (standard for SET receivers)
                return jsonify({'status': 'accepted', 'jti': payload.get('jti')}), 202

            except Exception as e:
                logger.error(f"❌ Failed to process SET: {str(e)}")
                return jsonify({
                    'err': 'invalid_request',
                    'description': f'Failed to process SET: {str(e)}'
                }), 400

        except Exception as e:
            logger.error(f"❌ Server error: {str(e)}", exc_info=True)
            return jsonify({'err': 'server_error', 'description': str(e)}), 500

    @bp.route('/events', methods=['GET'])
    def list_events():
        """List received events (for debugging)"""
        events = bp.event_processor.get_received_events()
        return jsonify({
            'total': len(events),
            'events': events
        })

    @bp.route('/events/clear', methods=['POST'])
    def clear_events():
        """Clear received events list"""
        bp.event_processor.clear_events()
        return jsonify({'status': 'cleared'})

    @bp.route('/health')
    def health():
        """Health check"""
        return jsonify({'status': 'healthy'})

    return bp
