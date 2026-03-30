"""
Formatted logging for received security events
"""

import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class EventLogger:
    """Formats and logs received security events"""

    def __init__(self):
        """Initialize event logger"""
        self.event_type_labels = {
            'device-risk-change': '📱 Device Risk Change',
            'ip-change': '🌐 IP Address Change',
            'user-risk-change': '👤 User Risk Change',
            'device-compliance-change': '🔒 Device Compliance Change',
            'session-revoked': '🚪 Session Revoked',
            'identifier-changed': '✉️  Identifier Changed'
        }

    def log_event(self, event_type_uri, event_data, issuer, jti, iat):
        """
        Log a received security event with formatted output

        Args:
            event_type_uri: Full event type URI
            event_data: Event data dictionary
            issuer: Issuer (Okta)
            jti: JWT ID
            iat: Issued at timestamp
        """
        # Extract event type name from URI
        event_type_name = event_type_uri.split('/')[-1]
        event_label = self.event_type_labels.get(event_type_name, f'📋 {event_type_name}')

        logger.info("┌" + "─" * 78 + "┐")
        logger.info(f"│ {event_label:76} │")
        logger.info("├" + "─" * 78 + "┤")

        # Log timestamp
        issued_time = datetime.fromtimestamp(iat).strftime('%Y-%m-%d %H:%M:%S') if iat else 'N/A'
        logger.info(f"│ 🕐 Received: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):62} │")
        logger.info(f"│ 🕐 Issued:   {issued_time:62} │")
        logger.info(f"│ 🔖 JTI:      {jti[:60]:62} │")

        # Log subject info
        subject = event_data.get('subject', {})
        user = subject.get('user', {})
        device = subject.get('device', {})

        if user:
            user_email = user.get('email', user.get('phone', 'N/A'))
            logger.info(f"│ 👤 User:     {user_email[:60]:62} │")

        if device:
            device_id = device.get('id', 'N/A')
            logger.info(f"│ 📱 Device:   {device_id[:60]:62} │")

        # Log event-specific fields
        logger.info("│" + "─" * 78 + "│")
        logger.info("│ Event Data:                                                              │")

        for key, value in event_data.items():
            if key == 'subject':
                continue

            # Format value for display
            if isinstance(value, dict):
                value_str = json.dumps(value)
            elif isinstance(value, int) and key == 'event_timestamp':
                # Convert Unix timestamp to readable date
                value_str = f"{value} ({datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')})"
            else:
                value_str = str(value)

            # Truncate if too long
            if len(value_str) > 55:
                value_str = value_str[:52] + "..."

            logger.info(f"│   {key:20} = {value_str:52} │")

        logger.info("└" + "─" * 78 + "┘")
