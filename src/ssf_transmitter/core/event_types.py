"""
SSF Event Type Definitions

Only the 6 event types that Okta officially supports as SSF receiver:
- device-risk-change (Okta)
- ip-change (Okta)
- user-risk-change (Okta)
- device-compliance-change (CAEP)
- session-revoked (CAEP)
- identifier-changed (RISC)
"""

# Field schemas for dynamic UI generation
FIELD_SCHEMAS = {
    # Risk level fields (for user/device risk change)
    'current_level': {
        'label': 'Current Risk Level',
        'type': 'select',
        'hint': 'Current risk level',
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
        'hint': 'Previous risk level',
        'options': [
            {'value': 'low', 'label': 'Low Risk'},
            {'value': 'medium', 'label': 'Medium Risk'},
            {'value': 'high', 'label': 'High Risk'}
        ],
        'placeholder': 'Select previous risk level...'
    },
    # IP address fields
    'current_ip_address': {
        'label': 'Current IP Address',
        'type': 'text',
        'hint': 'Current IP address of the user',
        'placeholder': 'e.g., 192.168.1.100'
    },
    'previous_ip_address': {
        'label': 'Previous IP Address',
        'type': 'text',
        'hint': 'Previous IP address of the user',
        'placeholder': 'e.g., 10.0.0.50'
    },
    # Device compliance fields
    'current_status': {
        'label': 'Current Compliance Status',
        'type': 'select',
        'hint': 'Current device compliance status',
        'options': [
            {'value': 'compliant', 'label': 'Compliant'},
            {'value': 'non-compliant', 'label': 'Non-Compliant'}
        ],
        'placeholder': 'Select status...'
    },
    'previous_status': {
        'label': 'Previous Compliance Status',
        'type': 'select',
        'hint': 'Previous device compliance status',
        'options': [
            {'value': 'compliant', 'label': 'Compliant'},
            {'value': 'non-compliant', 'label': 'Non-Compliant'}
        ],
        'placeholder': 'Select status...'
    },
    # Session revoked fields
    'current_ip': {
        'label': 'Current IP Address',
        'type': 'text',
        'hint': 'Current IP address for the session',
        'placeholder': 'e.g., 192.168.1.100'
    },
    'last_known_ip': {
        'label': 'Last Known IP Address',
        'type': 'text',
        'hint': 'Last known IP address',
        'placeholder': 'e.g., 10.0.0.50'
    },
    'current_user_agent': {
        'label': 'Current User Agent',
        'type': 'text',
        'hint': 'Current browser/client user agent',
        'placeholder': 'e.g., Mozilla/5.0...'
    },
    'last_known_user_agent': {
        'label': 'Last Known User Agent',
        'type': 'text',
        'hint': 'Last known user agent',
        'placeholder': 'e.g., Chrome/120.0.0.0'
    },
    # Device identifier fields
    'device_id': {
        'label': 'Device ID',
        'type': 'text',
        'hint': 'Device identifier',
        'placeholder': 'e.g., device-identifier-001'
    },
    # Identifier fields
    'new-value': {
        'label': 'New Identifier Value',
        'type': 'text',
        'hint': 'The new email address or phone number',
        'placeholder': 'new-email@example.com'
    },
    # Common fields
    'event_timestamp': {
        'label': 'Event Timestamp',
        'type': 'datetime-local',
        'hint': 'When the event occurred',
        'placeholder': '',
        'convert_to': 'unix_timestamp'
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
        'hint': 'Administrator-facing reason',
        'placeholder': 'e.g., critical security activity detected'
    },
    'reason_user': {
        'label': 'User Reason',
        'type': 'text',
        'hint': 'User-facing reason',
        'placeholder': 'e.g., We detected suspicious activity'
    }
}

# Only the 6 event types that Okta actually supports
EVENT_TYPES = {
    # === Okta-Specific Events ===
    'DEVICE_RISK_CHANGE': {
        'uri': 'https://schemas.okta.com/secevent/okta/event-type/device-risk-change',
        'label': 'Device Risk Change',
        'description': 'Signal changes in device risk level (e.g., trusted device becomes suspicious)',
        'category': 'Okta Events',
        'extra_fields': [
            {'name': 'device_id', 'required': True},
            {'name': 'current_level', 'required': True},
            {'name': 'previous_level', 'required': True},
            {'name': 'event_timestamp', 'required': False},
            {'name': 'initiating_entity', 'required': False},
            {'name': 'reason_admin', 'required': False},
            {'name': 'reason_user', 'required': False}
        ]
    },

    'IP_CHANGE': {
        'uri': 'https://schemas.okta.com/secevent/okta/event-type/ip-change',
        'label': 'IP Address Change',
        'description': 'User IP address has changed (e.g., user logged in from new location)',
        'category': 'Okta Events',
        'extra_fields': [
            {'name': 'device_id', 'required': True},
            {'name': 'current_ip_address', 'required': True},
            {'name': 'previous_ip_address', 'required': False},
            {'name': 'event_timestamp', 'required': False},
            {'name': 'initiating_entity', 'required': False},
            {'name': 'reason_admin', 'required': False},
            {'name': 'reason_user', 'required': False}
        ]
    },

    'USER_RISK_CHANGE': {
        'uri': 'https://schemas.okta.com/secevent/okta/event-type/user-risk-change',
        'label': 'User Risk Change',
        'description': 'Signal changes in user risk level (e.g., low → high)',
        'category': 'Okta Events',
        'extra_fields': [
            {'name': 'device_id', 'required': True},
            {'name': 'current_level', 'required': True},
            {'name': 'previous_level', 'required': True},
            {'name': 'event_timestamp', 'required': False},
            {'name': 'initiating_entity', 'required': False},
            {'name': 'reason_admin', 'required': False},
            {'name': 'reason_user', 'required': False}
        ]
    },

    # === CAEP (Continuous Access Evaluation Profile) Events ===
    'DEVICE_COMPLIANCE_CHANGE': {
        'uri': 'https://schemas.openid.net/secevent/caep/event-type/device-compliance-change',
        'label': 'Device Compliance Change',
        'description': 'Device compliance status has changed (e.g., device no longer meets security requirements)',
        'category': 'CAEP Events',
        'extra_fields': [
            {'name': 'device_id', 'required': True},
            {'name': 'current_status', 'required': True},
            {'name': 'previous_status', 'required': False},
            {'name': 'event_timestamp', 'required': False},
            {'name': 'initiating_entity', 'required': False},
            {'name': 'reason_admin', 'required': False},
            {'name': 'reason_user', 'required': False}
        ]
    },

    'SESSION_REVOKED': {
        'uri': 'https://schemas.openid.net/secevent/caep/event-type/session-revoked',
        'label': 'Session Revoked',
        'description': 'User session has been revoked (e.g., force logout due to security event)',
        'category': 'CAEP Events',
        'extra_fields': [
            {'name': 'device_id', 'required': True},
            {'name': 'current_ip', 'required': False},
            {'name': 'last_known_ip', 'required': False},
            {'name': 'current_user_agent', 'required': False},
            {'name': 'last_known_user_agent', 'required': False},
            {'name': 'event_timestamp', 'required': False},
            {'name': 'initiating_entity', 'required': False},
            {'name': 'reason_admin', 'required': False},
            {'name': 'reason_user', 'required': False}
        ]
    },

    # === RISC (Risk and Incident Sharing) Events ===
    'IDENTIFIER_CHANGED': {
        'uri': 'https://schemas.openid.net/secevent/risc/event-type/identifier-changed',
        'label': 'Identifier Changed',
        'description': 'User identifier (email/phone) has been modified',
        'category': 'RISC Events',
        'extra_fields': [
            {'name': 'device_id', 'required': True},
            {'name': 'new-value', 'required': False},
            {'name': 'event_timestamp', 'required': False}
        ]
    }
}


def get_event_type(event_type_key):
    """Get event type by key"""
    return EVENT_TYPES.get(event_type_key)


def get_event_uri(event_type_key):
    """Get event URI by key"""
    event_type = get_event_type(event_type_key)
    return event_type['uri'] if event_type else None


def validate_event_type(event_type_key):
    """Validate event type key"""
    return event_type_key in EVENT_TYPES


def get_event_types_by_category():
    """Get event types grouped by category"""
    categories = {}
    for key, event in EVENT_TYPES.items():
        category = event.get('category', 'Other')
        if category not in categories:
            categories[category] = {}
        categories[category][key] = event
    return categories


def get_field_schema(field_name):
    """Get field schema for UI generation"""
    return FIELD_SCHEMAS.get(field_name)


def get_required_fields(event_type_key):
    """Get required field names for an event type"""
    event_type = get_event_type(event_type_key)
    if not event_type:
        return []

    extra_fields = event_type.get('extra_fields', [])
    return [field['name'] for field in extra_fields if field.get('required', False)]


def get_event_type_with_schemas(event_type_key):
    """Get event type with full field schemas for UI generation"""
    event_type = get_event_type(event_type_key)
    if not event_type:
        return None

    result = dict(event_type)
    result['field_definitions'] = []

    for field in event_type.get('extra_fields', []):
        field_def = dict(field)
        schema = get_field_schema(field['name'])
        if schema:
            field_def.update(schema)
        result['field_definitions'].append(field_def)

    return result
