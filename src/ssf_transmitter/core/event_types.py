"""
SSF Event Type Definitions

Based on OpenID RISC (Risk and Incident Sharing and Coordination) Profile
and Okta-specific event types.
"""

# Complete RISC Event Types + Okta Custom Types
EVENT_TYPES = {
    # === Account Security Events ===
    'CREDENTIAL_CHANGE_REQUIRED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required',
        'label': 'Credential Change Required',
        'description': 'User was required to update their credentials (e.g., password change)',
        'category': 'Account Security',
        'fields': {'reason': 'optional'}
    },
    'CREDENTIAL_COMPROMISE': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/credential-compromise',
        'label': 'Credential Compromise',
        'description': 'A credential associated with an identifier has been compromised',
        'category': 'Account Security',
        'fields': {'credential_type': 'required', 'reason': 'optional'}
    },
    'ACCOUNT_DISABLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-disabled',
        'label': 'Account Disabled',
        'description': 'Account has been deactivated due to security concerns',
        'category': 'Account Security',
        'fields': {'reason': 'optional'}
    },
    'ACCOUNT_ENABLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-enabled',
        'label': 'Account Enabled',
        'description': 'Previously disabled account has been re-enabled',
        'category': 'Account Security',
        'fields': {'reason': 'optional'}
    },
    'ACCOUNT_PURGED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-purged',
        'label': 'Account Purged',
        'description': 'Account has been permanently deleted',
        'category': 'Account Security',
        'fields': {'reason': 'optional'}
    },

    # === Identifier Events ===
    'IDENTIFIER_CHANGED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/identifier-changed',
        'label': 'Identifier Changed',
        'description': 'User identifier (email/phone) has been modified',
        'category': 'Identifier Management',
        'fields': {'new-value': 'optional', 'reason': 'optional'}
    },
    'IDENTIFIER_RECYCLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/identifier-recycled',
        'label': 'Identifier Recycled',
        'description': 'Identifier was recycled and now belongs to a new user',
        'category': 'Identifier Management',
        'fields': {'reason': 'optional'}
    },

    # === Recovery Events ===
    'RECOVERY_ACTIVATED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/recovery-activated',
        'label': 'Recovery Activated',
        'description': 'User activated an account recovery flow',
        'category': 'Recovery',
        'fields': {'reason': 'optional'}
    },
    'RECOVERY_INFORMATION_CHANGED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/recovery-information-changed',
        'label': 'Recovery Information Changed',
        'description': 'Recovery details (backup email/phone) have been modified',
        'category': 'Recovery',
        'fields': {'reason': 'optional'}
    },

    # === Opt-In/Out Events ===
    'OPT_IN': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/opt-in',
        'label': 'Opt In',
        'description': 'User opted into RISC event exchanges',
        'category': 'Opt-In/Out',
        'fields': {'reason': 'optional'}
    },
    'OPT_OUT_INITIATED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/opt-out-initiated',
        'label': 'Opt Out Initiated',
        'description': 'User requested exclusion from RISC event sharing',
        'category': 'Opt-In/Out',
        'fields': {'reason': 'optional'}
    },
    'OPT_OUT_CANCELLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/opt-out-cancelled',
        'label': 'Opt Out Cancelled',
        'description': 'User cancelled the opt-out request',
        'category': 'Opt-In/Out',
        'fields': {'reason': 'optional'}
    },
    'OPT_OUT_EFFECTIVE': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/opt-out-effective',
        'label': 'Opt Out Effective',
        'description': 'User was effectively opted out from RISC event exchanges',
        'category': 'Opt-In/Out',
        'fields': {'reason': 'optional'}
    },

    # === Session Events ===
    'SESSIONS_REVOKED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/sessions-revoked',
        'label': 'Sessions Revoked (Deprecated)',
        'description': 'All sessions for the account have been revoked',
        'category': 'Session Management',
        'fields': {'reason': 'optional'},
        'deprecated': True
    },

    # === Okta-Specific Events ===
    'USER_RISK_CHANGE': {
        'uri': 'https://schemas.okta.com/secevent/okta/event-type/user-risk-change',
        'label': 'User Risk Change (Okta)',
        'description': 'User risk level has changed (e.g., LOW → HIGH)',
        'category': 'Okta Specific',
        'fields': {
            'currentRiskLevel': 'required',
            'previousRiskLevel': 'required',
            'reason': 'optional'
        }
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


def get_event_types_by_category():
    """
    Get event types grouped by category

    Returns:
        dict: Event types organized by category
    """
    categories = {}
    for key, event in EVENT_TYPES.items():
        category = event.get('category', 'Other')
        if category not in categories:
            categories[category] = {}
        categories[category][key] = event
    return categories


def get_required_fields(event_type_key):
    """
    Get required fields for an event type

    Args:
        event_type_key: Event type key

    Returns:
        list: List of required field names
    """
    event_type = get_event_type(event_type_key)
    if not event_type:
        return []

    fields = event_type.get('fields', {})
    return [field for field, requirement in fields.items() if requirement == 'required']
