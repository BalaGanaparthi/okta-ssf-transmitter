"""
SSF Event Type Definitions
"""

EVENT_TYPES = {
    'CREDENTIAL_CHANGE_REQUIRED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required',
        'label': 'Credential Change Required',
        'description': 'User credentials are compromised and need to be changed'
    },
    'ACCOUNT_DISABLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-disabled',
        'label': 'Account Disabled',
        'description': 'User account should be disabled due to security concerns'
    },
    'ACCOUNT_ENABLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-enabled',
        'label': 'Account Enabled',
        'description': 'Previously disabled account is now safe to re-enable'
    }
}


def get_event_type(event_type_key):
    """
    Get event type by key

    Args:
        event_type_key: Event type key (e.g., 'CREDENTIAL_CHANGE_REQUIRED')

    Returns:
        Event type dictionary or None
    """
    return EVENT_TYPES.get(event_type_key)


def get_event_uri(event_type_key):
    """
    Get event URI by key

    Args:
        event_type_key: Event type key

    Returns:
        Event URI string or None
    """
    event_type = get_event_type(event_type_key)
    return event_type['uri'] if event_type else None


def validate_event_type(event_type_key):
    """
    Validate event type key

    Args:
        event_type_key: Event type key to validate

    Returns:
        bool: True if valid, False otherwise
    """
    return event_type_key in EVENT_TYPES
