"""
RSA Key Management for SSF Transmitter
"""

from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import base64
import logging

logger = logging.getLogger(__name__)


class KeyManager:
    """Manages RSA key pair for JWT signing"""

    def __init__(self, private_key_path, public_key_path):
        """
        Initialize KeyManager

        Args:
            private_key_path: Path to private key file
            public_key_path: Path to public key file
        """
        self.private_key_path = Path(private_key_path)
        self.public_key_path = Path(public_key_path)
        self._private_key = None
        self._public_key = None

    def ensure_keys_exist(self):
        """Verify RSA key pair exists - DO NOT auto-generate"""
        # Create directory if needed
        self.private_key_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.private_key_path.exists() or not self.public_key_path.exists():
            logger.error("=" * 70)
            logger.error("CRITICAL ERROR: RSA keys not found!")
            logger.error("=" * 70)
            logger.error(f"Private key path: {self.private_key_path}")
            logger.error(f"Public key path: {self.public_key_path}")
            logger.error("")
            logger.error("Keys are required and MUST be in the certs/ folder.")
            logger.error("Keys should be committed to git and deployed with the app.")
            logger.error("")
            logger.error("If you need to generate keys manually:")
            logger.error("  openssl genrsa -out certs/private_key.pem 2048")
            logger.error("  openssl rsa -in certs/private_key.pem -pubout -out certs/public_key.pem")
            logger.error("=" * 70)
            raise FileNotFoundError(
                f"RSA keys not found at {self.private_key_path} and {self.public_key_path}. "
                "Keys must exist in certs/ folder and be deployed with the application."
            )
        else:
            logger.info("✓ Keys found in certs/ folder")
            logger.info(f"  Private key: {self.private_key_path}")
            logger.info(f"  Public key: {self.public_key_path}")

            # Verify keys are valid
            try:
                self.get_private_key()
                self.get_public_key()
                logger.info("✓ Keys validated successfully")
            except Exception as e:
                logger.error(f"✗ Keys exist but are invalid: {e}")
                raise

    def _generate_keys(self):
        """Generate new RSA key pair"""
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Save private key
        with open(self.private_key_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Get public key
        public_key = private_key.public_key()

        # Save public key
        with open(self.public_key_path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        # Set permissions (restrictive)
        self.private_key_path.chmod(0o600)
        self.public_key_path.chmod(0o644)

    def get_private_key(self):
        """
        Get private key for signing

        Returns:
            str: Private key in PEM format
        """
        if self._private_key is None:
            with open(self.private_key_path, 'r') as f:
                self._private_key = f.read()
        return self._private_key

    def get_public_key(self):
        """
        Get public key

        Returns:
            Public key object
        """
        if self._public_key is None:
            with open(self.public_key_path, 'rb') as f:
                self._public_key = serialization.load_pem_public_key(
                    f.read(),
                    backend=default_backend()
                )
        return self._public_key

    def get_jwks(self, key_id):
        """
        Generate JWKS from public key

        Args:
            key_id: Key identifier

        Returns:
            dict: JWKS dictionary
        """
        public_key = self.get_public_key()
        public_numbers = public_key.public_numbers()

        def int_to_base64url(num):
            """Convert integer to base64url encoding"""
            num_bytes = num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')
            return base64.urlsafe_b64encode(num_bytes).rstrip(b'=').decode('utf-8')

        return {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "kid": key_id,
                    "alg": "RS256",
                    "n": int_to_base64url(public_numbers.n),
                    "e": int_to_base64url(public_numbers.e)
                }
            ]
        }
