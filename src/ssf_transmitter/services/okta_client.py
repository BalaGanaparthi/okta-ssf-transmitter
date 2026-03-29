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
        logger.info(f"Sending SET to {self.endpoint}")

        try:
            response = requests.post(
                self.endpoint,
                data=set_token,
                headers={'Content-Type': 'application/secevent+jwt'},
                timeout=self.timeout
            )

            response.raise_for_status()

            logger.info(f"SET accepted by Okta (Status: {response.status_code})")

            return {
                'success': True,
                'status': response.status_code,
                'data': response.json() if response.content else None
            }

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error sending SET: {e.response.status_code}")
            error_data = None
            try:
                error_data = e.response.json()
            except:
                error_data = e.response.text

            return {
                'success': False,
                'status': e.response.status_code,
                'error': error_data
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return {
                'success': False,
                'error': 'Request failed',
                'details': str(e)
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
