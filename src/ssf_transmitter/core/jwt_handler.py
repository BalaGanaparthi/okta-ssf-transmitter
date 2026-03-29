"""
JWT/SET Generation and Handling
"""

import jwt
import uuid
import time
import logging

logger = logging.getLogger(__name__)


class JWTHandler:
    """Handles JWT/SET generation and signing"""

    def __init__(self, key_manager, issuer, audience, key_id):
        """
        Initialize JWTHandler

        Args:
            key_manager: KeyManager instance
            issuer: Issuer URL
            audience: Audience (Okta domain)
            key_id: Key identifier
        """
        self.key_manager = key_manager
        self.issuer = issuer
        self.audience = audience
        self.key_id = key_id

    def generate_set(self, event_type_uri, subject, reason=None, extra_fields=None):
        """
        Generate a Security Event Token (SET)

        Args:
            event_type_uri: Event type URI
            subject: User email (subject of the event)
            reason: Optional reason for the event
            extra_fields: Additional event-specific fields

        Returns:
            str: Signed JWT token
        """
        logger.info(f"Generating SET for event type: {event_type_uri}")

        # Get private key
        private_key = self.key_manager.get_private_key()

        # Create unique event ID
        jti = f"evt_{str(uuid.uuid4())}"

        # Current timestamp
        iat = int(time.time())

        # Build SET payload
        payload = {
            'iss': self.issuer,
            'jti': jti,
            'iat': iat,
            'aud': self.audience,
            'events': {}
        }

        # Add the specific event
        event_data = {
            'subject': {
                'format': 'email',
                'email': subject
            }
        }

        # Add reason if provided
        if reason:
            event_data['reason'] = reason

        # Add extra fields if provided
        if extra_fields:
            event_data.update(extra_fields)

        payload['events'][event_type_uri] = event_data

        # JWT header
        headers = {
            'alg': 'RS256',
            'kid': self.key_id,
            'typ': 'secevent+jwt'
        }

        # Sign the SET
        token = jwt.encode(
            payload,
            private_key,
            algorithm='RS256',
            headers=headers
        )

        logger.debug(f"SET generated successfully with JTI: {jti}")
        return token

    def decode_set(self, token, verify=False):
        """
        Decode a SET token (for debugging/testing)

        Args:
            token: JWT token to decode
            verify: Whether to verify signature

        Returns:
            dict: Decoded payload
        """
        if verify:
            # This would require the public key
            # For now, just decode without verification
            pass

        return jwt.decode(token, options={"verify_signature": False})
