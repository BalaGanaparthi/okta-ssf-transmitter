"""
Process received Security Event Tokens
"""

import logging
from datetime import datetime
from ..services.event_logger import EventLogger

logger = logging.getLogger(__name__)


class EventProcessor:
    """Process and log received SETs"""

    def __init__(self):
        """Initialize event processor"""
        self.event_logger = EventLogger()
        self.processed_count = 0
        self.received_events = []

    def process_set(self, header, payload, token):
        """
        Process a received SET

        Args:
            header: JWT header
            payload: JWT payload (decoded)
            token: Raw JWT token string

        Returns:
            dict: Processing result
        """
        try:
            # Extract metadata
            issuer = payload.get('iss', 'Unknown')
            jti = payload.get('jti', 'Unknown')
            iat = payload.get('iat', 0)
            events = payload.get('events', {})

            logger.info("=" * 80)
            logger.info("🎯 PROCESSING RECEIVED SET")
            logger.info("=" * 80)

            # Log each event in the SET
            for event_type_uri, event_data in events.items():
                self.event_logger.log_event(
                    event_type_uri=event_type_uri,
                    event_data=event_data,
                    issuer=issuer,
                    jti=jti,
                    iat=iat
                )

            # Store received event
            self.received_events.append({
                'received_at': datetime.now().isoformat(),
                'jti': jti,
                'issuer': issuer,
                'iat': iat,
                'event_count': len(events),
                'event_types': list(events.keys()),
                'token': token[:100] + '...' if len(token) > 100 else token,
                'header': header,
                'payload': payload
            })

            self.processed_count += 1

            logger.info("=" * 80)
            logger.info(f"✅ SET PROCESSING COMPLETE (Total processed: {self.processed_count})")
            logger.info("=" * 80)

            return {
                'status': 'processed',
                'events_count': len(events),
                'jti': jti
            }

        except Exception as e:
            logger.error(f"Error processing SET: {str(e)}", exc_info=True)
            raise

    def get_received_events(self):
        """Get list of received events"""
        return self.received_events

    def clear_events(self):
        """Clear received events list"""
        self.received_events = []
        self.processed_count = 0
