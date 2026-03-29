"""
Validation utilities
"""

import re
from urllib.parse import urlparse


def validate_email(email):
    """
    Validate email format

    Args:
        email: Email address to validate

    Returns:
        bool: True if valid email format
    """
    if not email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url):
    """
    Validate URL format

    Args:
        url: URL to validate

    Returns:
        bool: True if valid URL format
    """
    if not url:
        return False

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def validate_set_payload(payload):
    """
    Validate SET payload structure

    Args:
        payload: SET payload dictionary

    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['subject', 'eventType']

    for field in required_fields:
        if field not in payload:
            return False, f"Missing required field: {field}"

    # Validate email
    if not validate_email(payload['subject']):
        return False, "Invalid email format"

    return True, None
