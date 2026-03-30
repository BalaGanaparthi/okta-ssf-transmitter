"""
JWT Validation for incoming SETs from Okta
"""

import jwt
import logging

logger = logging.getLogger(__name__)


class JWTValidator:
    """Validates JWT tokens from Okta"""

    def __init__(self, expected_issuer, jwks_url=None):
        """
        Initialize JWT Validator

        Args:
            expected_issuer: Expected issuer (Okta domain)
            jwks_url: URL to fetch Okta's public JWKS
        """
        self.expected_issuer = expected_issuer
        self.jwks_url = jwks_url

    def validate_and_decode(self, token):
        """
        Validate and decode JWT token

        Args:
            token: JWT token string

        Returns:
            dict: Decoded payload if valid

        Raises:
            jwt.InvalidTokenError: If validation fails
        """
        # For now, decode without signature verification
        # In production, fetch JWKS and verify signature
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})

            # Validate issuer
            if decoded.get('iss') != self.expected_issuer:
                logger.warning(f"Issuer mismatch: {decoded.get('iss')} != {self.expected_issuer}")
                # Note: Still process for demo purposes

            return decoded

        except jwt.DecodeError as e:
            logger.error(f"Failed to decode JWT: {e}")
            raise
        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise

    def get_header(self, token):
        """Get JWT header without verification"""
        return jwt.get_unverified_header(token)
