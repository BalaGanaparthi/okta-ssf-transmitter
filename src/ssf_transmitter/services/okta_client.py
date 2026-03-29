"""
Okta API Client
"""

import requests
import logging

logger = logging.getLogger(__name__)


class OktaClient:
    """Client for sending SETs to Okta"""

    def __init__(self, okta_domain, timeout=10):
        """
        Initialize Okta client

        Args:
            okta_domain: Okta organization domain
            timeout: Request timeout in seconds
        """
        self.okta_domain = okta_domain
        self.timeout = timeout
        self.endpoint = f"{okta_domain}/security/api/v1/security-events"

    def send_set(self, set_token):
        """
        Send a SET to Okta

        Args:
            set_token: Signed JWT token

        Returns:
            dict: Response dictionary with success status
        """
        import time
        start_time = time.time()

        logger.info("=" * 70)
        logger.info("🚀 TRANSMITTING TO OKTA")
        logger.info("=" * 70)
        logger.info(f"Endpoint: {self.endpoint}")
        logger.info(f"Token length: {len(set_token)} bytes")
        logger.info(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            logger.info("Making HTTP POST request to Okta...")

            response = requests.post(
                self.endpoint,
                data=set_token,
                headers={'Content-Type': 'application/secevent+jwt'},
                timeout=self.timeout
            )

            elapsed = time.time() - start_time
            logger.info(f"Received response from Okta in {elapsed:.2f}s")

            response.raise_for_status()

            logger.info("=" * 70)
            logger.info(f"✅ SUCCESS: SET accepted by Okta")
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response: {response.text[:200] if response.text else 'No content'}")
            logger.info("=" * 70)

            return {
                'success': True,
                'status': response.status_code,
                'data': response.json() if response.content else None,
                'transmission_time': elapsed
            }

        except requests.exceptions.HTTPError as e:
            elapsed = time.time() - start_time

            logger.error("=" * 70)
            logger.error(f"❌ OKTA REJECTED SET")
            logger.error("=" * 70)
            logger.error(f"HTTP Status: {e.response.status_code}")
            logger.error(f"Response Time: {elapsed:.2f}s")
            logger.error(f"Full Response: {e.response.text}")

            error_data = None
            try:
                error_data = e.response.json()
                logger.error(f"Parsed Error: {error_data}")
            except:
                error_data = e.response.text

            logger.error("=" * 70)
            logger.error("⚠️  NOTE: Rejected events do NOT appear in Okta System Log")
            logger.error("⚠️  Only successfully accepted events (202) are logged by Okta")
            logger.error("=" * 70)

            return {
                'success': False,
                'status': e.response.status_code,
                'error': error_data,
                'okta_response': True,  # Flag to confirm this is from Okta, not hardcoded
                'endpoint': self.endpoint,
                'transmission_time': elapsed,
                'note': 'Rejected events do not appear in Okta System Log'
            }

        except requests.exceptions.RequestException as e:
            elapsed = time.time() - start_time

            logger.error("=" * 70)
            logger.error(f"❌ NETWORK ERROR")
            logger.error("=" * 70)
            logger.error(f"Error: {str(e)}")
            logger.error(f"Time elapsed: {elapsed:.2f}s")
            logger.error("=" * 70)

            return {
                'success': False,
                'error': 'Request failed',
                'details': str(e),
                'transmission_time': elapsed
            }

    def validate_connection(self):
        """
        Validate connection to Okta (health check)

        Returns:
            bool: True if connection successful
        """
        try:
            # Simple check - just verify domain is reachable
            response = requests.head(self.okta_domain, timeout=5)
            return response.status_code < 500
        except:
            return False
