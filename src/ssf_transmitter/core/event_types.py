"""
SSF Event Type Definitions

Based on OpenID RISC (Risk and Incident Sharing and Coordination) Profile
and Okta-specific event types.

Each event type includes a schema for dynamic UI generation.
"""

# Field schemas for dynamic UI generation
FIELD_SCHEMAS = {
    'current_level': {
        'label': 'Current Risk Level',
        'type': 'select',
        'hint': 'Current risk level of the user',
        'options': [
            {'value': 'low', 'label': 'Low Risk'},
            {'value': 'medium', 'label': 'Medium Risk'},
            {'value': 'high', 'label': 'High Risk'}
        ],
        'placeholder': 'Select current risk level...'
    },
    'previous_level': {
        'label': 'Previous Risk Level',
        'type': 'select',
        'hint': 'Previous risk level of the user',
        'options': [
            {'value': 'low', 'label': 'Low Risk'},
            {'value': 'medium', 'label': 'Medium Risk'},
            {'value': 'high', 'label': 'High Risk'}
        ],
        'placeholder': 'Select previous risk level...'
    },
    'credential_type': {
        'label': 'Credential Type',
        'type': 'select',
        'hint': 'Type of credential that was compromised',
        'options': [
            {'value': 'password', 'label': 'Password'},
            {'value': 'token', 'label': 'Access Token'},
            {'value': 'api_key', 'label': 'API Key'},
            {'value': 'ssh_key', 'label': 'SSH Key'},
            {'value': 'certificate', 'label': 'Certificate'},
            {'value': 'session', 'label': 'Session Token'},
            {'value': 'oauth_token', 'label': 'OAuth Token'},
            {'value': 'bearer_token', 'label': 'Bearer Token'}
        ],
        'placeholder': 'Select credential type...'
    },
    'new-value': {
        'label': 'New Identifier Value',
        'type': 'text',
        'hint': 'The new email address or phone number',
        'placeholder': 'new-email@example.com'
    },
    'reason': {
        'label': 'Reason',
        'type': 'select',
        'hint': 'Reason for account disability',
        'options': [
            {'value': 'hijacking', 'label': 'Account Hijacking'},
            {'value': 'bulk-account', 'label': 'Bulk Account Issue'}
        ],
        'placeholder': 'Select reason...'
    },
    'event_timestamp': {
        'label': 'Event Timestamp',
        'type': 'number',
        'hint': 'When the event occurred (Unix timestamp)',
        'placeholder': 'e.g., 1711699200'
    },
    'initiating_entity': {
        'label': 'Initiating Entity',
        'type': 'select',
        'hint': 'Who initiated this event',
        'options': [
            {'value': 'admin', 'label': 'Administrator'},
            {'value': 'system', 'label': 'System'},
            {'value': 'user', 'label': 'User'}
        ],
        'placeholder': 'Select entity...'
    },
    'reason_admin': {
        'label': 'Admin Reason',
        'type': 'text',
        'hint': 'Administrator-facing reason (English)',
        'placeholder': 'e.g., critical security activity detected'
    },
    'reason_user': {
        'label': 'User Reason',
        'type': 'text',
        'hint': 'User-facing reason (English)',
        'placeholder': 'e.g., We detected suspicious activity'
    }
}

# Complete RISC Event Types + Okta Custom Types with field schemas
EVENT_TYPES = {
    # === Account Security Events ===
    'CREDENTIAL_CHANGE_REQUIRED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required',
        'label': 'Credential Change Required',
        'description': 'User was required to update their credentials (e.g., password change)',
        'category': 'Account Security',
        'extra_fields': []
    },
    'CREDENTIAL_COMPROMISE': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/credential-compromise',
        'label': 'Credential Compromise',
        'description': 'A credential associated with an identifier has been compromised',
        'category': 'Account Security',
        'extra_fields': [
            {'name': 'credential_type', 'required': True},
            {'name': 'event_timestamp', 'required': False},
            {'name': 'reason_admin', 'required': False},
            {'name': 'reason_user', 'required': False}
        ]
    },
    'ACCOUNT_DISABLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-disabled',
        'label': 'Account Disabled',
        'description': 'Account has been deactivated due to security concerns',
        'category': 'Account Security',
        'extra_fields': [
            {'name': 'reason', 'required': False, 'note': 'Can be "hijacking" or "bulk-account"'}
        ]
    },
    'ACCOUNT_ENABLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-enabled',
        'label': 'Account Enabled',
        'description': 'Previously disabled account has been re-enabled',
        'category': 'Account Security',
        'extra_fields': []
    },
    'ACCOUNT_PURGED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/account-purged',
        'label': 'Account Purged',
        'description': 'Account has been permanently deleted',
        'category': 'Account Security',
        'extra_fields': []
    },

    # === Identifier Events ===
    'IDENTIFIER_CHANGED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/identifier-changed',
        'label': 'Identifier Changed',
        'description': 'User identifier (email/phone) has been modified',
        'category': 'Identifier Management',
        'extra_fields': [
            {'name': 'new-value', 'required': False}
        ]
    },
    'IDENTIFIER_RECYCLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/identifier-recycled',
        'label': 'Identifier Recycled',
        'description': 'Identifier was recycled and now belongs to a new user',
        'category': 'Identifier Management',
        'extra_fields': []
    },

    # === Recovery Events ===
    'RECOVERY_ACTIVATED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/recovery-activated',
        'label': 'Recovery Activated',
        'description': 'User activated an account recovery flow',
        'category': 'Recovery',
        'extra_fields': []
    },
    'RECOVERY_INFORMATION_CHANGED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/recovery-information-changed',
        'label': 'Recovery Information Changed',
        'description': 'Recovery details (backup email/phone) have been modified',
        'category': 'Recovery',
        'extra_fields': []
    },

    # === Opt-In/Out Events ===
    'OPT_IN': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/opt-in',
        'label': 'Opt In',
        'description': 'User opted into RISC event exchanges',
        'category': 'Opt-In/Out',
        'extra_fields': []
    },
    'OPT_OUT_INITIATED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/opt-out-initiated',
        'label': 'Opt Out Initiated',
        'description': 'User requested exclusion from RISC event sharing',
        'category': 'Opt-In/Out',
        'extra_fields': []
    },
    'OPT_OUT_CANCELLED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/opt-out-cancelled',
        'label': 'Opt Out Cancelled',
        'description': 'User cancelled the opt-out request',
        'category': 'Opt-In/Out',
        'extra_fields': []
    },
    'OPT_OUT_EFFECTIVE': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/opt-out-effective',
        'label': 'Opt Out Effective',
        'description': 'User was effectively opted out from RISC event exchanges',
        'category': 'Opt-In/Out',
        'extra_fields': []
    },

    # === Session Events ===
    'SESSIONS_REVOKED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/sessions-revoked',
        'label': 'Sessions Revoked (Deprecated)',
        'description': 'All sessions for the account have been revoked',
        'category': 'Session Management',
        'extra_fields': [],
        'deprecated': True
    },

    # === Okta-Specific Events ===
    'USER_RISK_CHANGE': {
        'uri': 'https://schemas.okta.com/secevent/okta/event-type/user-risk-change',
        'label': 'User Risk Change (Okta)',
        'description': 'User risk level has changed (e.g., low → high)',
        'category': 'Okta Specific',
        'extra_fields': [
            {'name': 'current_level', 'required': True},
            {'name': 'previous_level', 'required': True},
            {'name': 'event_timestamp', 'required': False},
            {'name': 'initiating_entity', 'required': False},
            {'name': 'reason_admin', 'required': False},
            {'name': 'reason_user', 'required': False}
        ]
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


def get_field_schema(field_name):
    """
    Get field schema for UI generation

    Args:
        field_name: Name of the field

    Returns:
        dict: Field schema or None
    """
    return FIELD_SCHEMAS.get(field_name)


def get_required_fields(event_type_key):
    """
    Get required field names for an event type

    Args:
        event_type_key: Event type key

    Returns:
        list: List of required field names
    """
    event_type = get_event_type(event_type_key)
    if not event_type:
        return []

    extra_fields = event_type.get('extra_fields', [])
    return [field['name'] for field in extra_fields if field.get('required', False)]


def get_event_type_with_schemas(event_type_key):
    """
    Get event type with full field schemas for UI generation

    Args:
        event_type_key: Event type key

    Returns:
        dict: Event type with resolved field schemas
    """
    event_type = get_event_type(event_type_key)
    if not event_type:
        return None

    # Clone the event type
    result = dict(event_type)

    # Add resolved field schemas
    result['field_definitions'] = []
    for field in event_type.get('extra_fields', []):
        field_def = dict(field)
        schema = get_field_schema(field['name'])
        if schema:
            field_def.update(schema)
        result['field_definitions'].append(field_def)

    return result
