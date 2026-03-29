"""
SSF Transmitter Example - Send Security Event Tokens to Okta (Python)

This example demonstrates how to:
1. Generate a Security Event Token (SET)
2. Sign it with RS256
3. Send it to Okta as a risk signal
"""

import jwt
import requests
import uuid
import time
from datetime import datetime
from typing import Dict, Optional

# ============================================================================
# Configuration
# ============================================================================

CONFIG = {
    # Your transmitter details
    'issuer': 'https://mysystem.example.com',
    'private_key_path': './private_key.pem',  # Path to your RS256 private key
    'key_id': 'transmitter-key-1',  # Must match the kid in your JWKS

    # Okta receiver details
    'okta_domain': 'https://your-org.okta.com',
    'okta_set_endpoint': 'https://your-org.okta.com/security/api/v1/security-events',
}

# ============================================================================
# Supported Event Types
# ============================================================================

EVENT_TYPES = {
    'CREDENTIAL_CHANGE_REQUIRED': 'https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required',
    'ACCOUNT_DISABLED': 'https://schemas.openid.net/secevent/risc/event-type/account-disabled',
    'ACCOUNT_ENABLED': 'https://schemas.openid.net/secevent/risc/event-type/account-enabled',
}

# ============================================================================
# SET Generator
# ============================================================================

def generate_set(event_type: str, user_email: str, reason: Optional[str] = None) -> str:
    """
    Generate a Security Event Token (SET)

    Args:
        event_type: One of the EVENT_TYPES
        user_email: Email of the affected user in Okta
        reason: Human-readable reason for the event

    Returns:
        Signed JWT (SET) as a string
    """
    # Read private key
    with open(CONFIG['private_key_path'], 'r') as key_file:
        private_key = key_file.read()

    # Create unique event ID
    jti = f"evt_{str(uuid.uuid4())}"

    # Current timestamp
    iat = int(time.time())

    # Build SET payload
    payload = {
        'iss': CONFIG['issuer'],
        'jti': jti,
        'iat': iat,
        'aud': CONFIG['okta_domain'],
        'events': {}
    }

    # Add the specific event
    event_data = {
        'subject': {
            'format': 'email',
            'email': user_email
        }
    }

    # Add reason if provided
    if reason:
        event_data['reason'] = reason

    payload['events'][event_type] = event_data

    # JWT header
    headers = {
        'alg': 'RS256',
        'kid': CONFIG['key_id'],
        'typ': 'secevent+jwt'
    }

    # Sign the SET
    token = jwt.encode(
        payload,
        private_key,
        algorithm='RS256',
        headers=headers
    )

    return token

# ============================================================================
# SET Transmitter
# ============================================================================

def send_set(set_token: str) -> Dict:
    """
    Send a SET to Okta

    Args:
        set_token: The signed JWT token

    Returns:
        Dictionary with response details
    """
    try:
        response = requests.post(
            CONFIG['okta_set_endpoint'],
            data=set_token,
            headers={
                'Content-Type': 'application/secevent+jwt'
            },
            timeout=10  # 10 second timeout
        )

        response.raise_for_status()

        return {
            'success': True,
            'status': response.status_code,
            'data': response.json() if response.content else None
        }

    except requests.exceptions.HTTPError as e:
        return {
            'success': False,
            'status': e.response.status_code,
            'error': e.response.json() if e.response.content else str(e)
        }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': 'Request failed',
            'details': str(e)
        }

# ============================================================================
# High-Level Functions
# ============================================================================

def report_compromised_credentials(user_email: str, reason: str) -> Dict:
    """
    Report compromised credentials for a user

    Args:
        user_email: User's email address
        reason: Why credentials are compromised

    Returns:
        Response dictionary
    """
    print(f"🔒 Reporting compromised credentials for: {user_email}")

    set_token = generate_set(
        EVENT_TYPES['CREDENTIAL_CHANGE_REQUIRED'],
        user_email,
        reason
    )

    result = send_set(set_token)

    if result['success']:
        print(f"✅ SET accepted by Okta (Status: {result['status']})")
    else:
        print(f"❌ SET rejected (Status: {result.get('status', 'N/A')}): {result.get('error')}")

    return result

def disable_account(user_email: str, reason: str) -> Dict:
    """
    Request Okta to disable a user account

    Args:
        user_email: User's email address
        reason: Why account should be disabled

    Returns:
        Response dictionary
    """
    print(f"🚫 Requesting account disable for: {user_email}")

    set_token = generate_set(
        EVENT_TYPES['ACCOUNT_DISABLED'],
        user_email,
        reason
    )

    result = send_set(set_token)

    if result['success']:
        print(f"✅ SET accepted by Okta (Status: {result['status']})")
    else:
        print(f"❌ SET rejected (Status: {result.get('status', 'N/A')}): {result.get('error')}")

    return result

def enable_account(user_email: str, reason: str) -> Dict:
    """
    Notify Okta that a previously disabled account is now safe

    Args:
        user_email: User's email address
        reason: Why account is now safe

    Returns:
        Response dictionary
    """
    print(f"✅ Requesting account enable for: {user_email}")

    set_token = generate_set(
        EVENT_TYPES['ACCOUNT_ENABLED'],
        user_email,
        reason
    )

    result = send_set(set_token)

    if result['success']:
        print(f"✅ SET accepted by Okta (Status: {result['status']})")
    else:
        print(f"❌ SET rejected (Status: {result.get('status', 'N/A')}): {result.get('error')}")

    return result

# ============================================================================
# Example Usage
# ============================================================================

def main():
    print('=== SSF Transmitter Example ===\n')

    # Example 1: Report compromised credentials
    report_compromised_credentials(
        'john.doe@example.com',
        'Password found in HaveIBeenPwned database breach'
    )

    print('\n---\n')

    # Example 2: Disable account due to suspicious activity
    disable_account(
        'jane.smith@example.com',
        'Multiple failed login attempts from suspicious IP addresses'
    )

    print('\n---\n')

    # Example 3: Re-enable account after investigation
    enable_account(
        'jane.smith@example.com',
        'Investigation completed - activity confirmed as legitimate'
    )

if __name__ == '__main__':
    main()
