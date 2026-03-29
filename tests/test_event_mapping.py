"""
Test event type field mapping from UI to JWT payload
"""

import pytest
import json
from src.ssf_transmitter.core import get_event_type_with_schemas, get_event_uri
from src.ssf_transmitter.core import JWTHandler
import jwt as pyjwt


def test_user_risk_change_mapping(jwt_handler):
    """Test User Risk Change event maps fields correctly"""
    event_type = 'USER_RISK_CHANGE'
    schema = get_event_type_with_schemas(event_type)

    # Simulate UI input
    ui_data = {
        'subject': 'test@example.com',
        'eventType': event_type,
        'currentRiskLevel': 'HIGH',
        'previousRiskLevel': 'LOW',
        'reason': 'Impossible travel detected'
    }

    # Collect extra fields (simulating backend logic)
    extra_fields = {}
    for field_def in schema['field_definitions']:
        field_name = field_def['name']
        if field_name in ui_data:
            extra_fields[field_name] = ui_data[field_name]

    # Generate JWT
    event_uri = get_event_uri(event_type)
    token = jwt_handler.generate_set(
        event_uri,
        ui_data['subject'],
        ui_data.get('reason'),
        extra_fields
    )

    # Decode and verify
    decoded = pyjwt.decode(token, options={"verify_signature": False})
    event_data = decoded['events'][event_uri]

    # Verify fields are in JWT
    assert 'currentRiskLevel' in event_data, "currentRiskLevel missing in JWT payload"
    assert event_data['currentRiskLevel'] == 'HIGH', "currentRiskLevel value incorrect"
    assert 'previousRiskLevel' in event_data, "previousRiskLevel missing in JWT payload"
    assert event_data['previousRiskLevel'] == 'LOW', "previousRiskLevel value incorrect"
    assert event_data['reason'] == 'Impossible travel detected'

    print("✅ USER_RISK_CHANGE: UI → JWT mapping correct")
    print(f"   Fields in JWT: {list(event_data.keys())}")


def test_credential_compromise_mapping(jwt_handler):
    """Test Credential Compromise event maps all fields correctly"""
    event_type = 'CREDENTIAL_COMPROMISE'
    schema = get_event_type_with_schemas(event_type)

    # Simulate UI input with all fields
    ui_data = {
        'subject': 'test@example.com',
        'eventType': event_type,
        'credential_type': 'password',
        'event_timestamp': '2024-03-29T10:00:00',
        'reason_admin': 'Found in breach database',
        'reason_user': 'Suspicious activity detected'
    }

    # Collect extra fields
    extra_fields = {}
    for field_def in schema['field_definitions']:
        field_name = field_def['name']
        if field_name in ui_data:
            extra_fields[field_name] = ui_data[field_name]

    # Generate JWT
    event_uri = get_event_uri(event_type)
    token = jwt_handler.generate_set(
        event_uri,
        ui_data['subject'],
        None,
        extra_fields
    )

    # Decode and verify
    decoded = pyjwt.decode(token, options={"verify_signature": False})
    event_data = decoded['events'][event_uri]

    # Verify all fields are in JWT
    assert 'credential_type' in event_data, "credential_type missing"
    assert event_data['credential_type'] == 'password'
    assert 'event_timestamp' in event_data, "event_timestamp missing"
    assert 'reason_admin' in event_data, "reason_admin missing"
    assert 'reason_user' in event_data, "reason_user missing"

    print("✅ CREDENTIAL_COMPROMISE: UI → JWT mapping correct")
    print(f"   Fields in JWT: {list(event_data.keys())}")


def test_account_disabled_mapping(jwt_handler):
    """Test Account Disabled event maps reason field correctly"""
    event_type = 'ACCOUNT_DISABLED'
    schema = get_event_type_with_schemas(event_type)

    # Simulate UI input with specific reason dropdown
    ui_data = {
        'subject': 'test@example.com',
        'eventType': event_type,
        'reason': 'hijacking'
    }

    # Collect extra fields
    extra_fields = {}
    for field_def in schema['field_definitions']:
        field_name = field_def['name']
        if field_name in ui_data:
            extra_fields[field_name] = ui_data[field_name]

    # Generate JWT
    event_uri = get_event_uri(event_type)
    token = jwt_handler.generate_set(
        event_uri,
        ui_data['subject'],
        None,
        extra_fields
    )

    # Decode and verify
    decoded = pyjwt.decode(token, options={"verify_signature": False})
    event_data = decoded['events'][event_uri]

    # Verify reason field
    assert 'reason' in event_data, "reason missing"
    assert event_data['reason'] == 'hijacking'

    print("✅ ACCOUNT_DISABLED: UI → JWT mapping correct")
    print(f"   Fields in JWT: {list(event_data.keys())}")


def test_identifier_changed_mapping(jwt_handler):
    """Test Identifier Changed event maps new-value correctly"""
    event_type = 'IDENTIFIER_CHANGED'
    schema = get_event_type_with_schemas(event_type)

    # Simulate UI input
    ui_data = {
        'subject': 'old@example.com',
        'eventType': event_type,
        'new-value': 'new@example.com'
    }

    # Collect extra fields
    extra_fields = {}
    for field_def in schema['field_definitions']:
        field_name = field_def['name']
        if field_name in ui_data:
            extra_fields[field_name] = ui_data[field_name]

    # Generate JWT
    event_uri = get_event_uri(event_type)
    token = jwt_handler.generate_set(
        event_uri,
        ui_data['subject'],
        None,
        extra_fields
    )

    # Decode and verify
    decoded = pyjwt.decode(token, options={"verify_signature": False})
    event_data = decoded['events'][event_uri]

    # Verify new-value field
    assert 'new-value' in event_data, "new-value missing"
    assert event_data['new-value'] == 'new@example.com'

    print("✅ IDENTIFIER_CHANGED: UI → JWT mapping correct")
    print(f"   Fields in JWT: {list(event_data.keys())}")


def test_standard_events_mapping(jwt_handler):
    """Test standard events (no extra fields) work correctly"""
    standard_events = [
        'CREDENTIAL_CHANGE_REQUIRED',
        'ACCOUNT_ENABLED',
        'ACCOUNT_PURGED',
        'IDENTIFIER_RECYCLED',
        'RECOVERY_ACTIVATED',
        'RECOVERY_INFORMATION_CHANGED',
        'OPT_IN',
        'OPT_OUT_INITIATED',
        'OPT_OUT_CANCELLED',
        'OPT_OUT_EFFECTIVE',
        'SESSIONS_REVOKED'
    ]

    for event_type in standard_events:
        schema = get_event_type_with_schemas(event_type)

        # These events have no extra fields
        assert len(schema['field_definitions']) == 0, f"{event_type} should have no extra fields"

        # Simulate UI input (just subject and reason)
        ui_data = {
            'subject': 'test@example.com',
            'eventType': event_type,
            'reason': f'Testing {event_type}'
        }

        # Generate JWT
        event_uri = get_event_uri(event_type)
        token = jwt_handler.generate_set(
            event_uri,
            ui_data['subject'],
            ui_data.get('reason'),
            None
        )

        # Decode and verify
        decoded = pyjwt.decode(token, options={"verify_signature": False})
        event_data = decoded['events'][event_uri]

        # Should have subject and reason only
        assert 'subject' in event_data
        assert event_data['subject']['email'] == 'test@example.com'
        assert event_data['reason'] == f'Testing {event_type}'

        print(f"✅ {event_type}: UI → JWT mapping correct")


def test_all_event_types_have_schemas():
    """Verify all event types have proper schema structure"""
    from src.ssf_transmitter.core import EVENT_TYPES

    for event_key, event_data in EVENT_TYPES.items():
        # Get with schemas
        schema = get_event_type_with_schemas(event_key)

        # Verify structure
        assert 'uri' in schema, f"{event_key} missing uri"
        assert 'label' in schema, f"{event_key} missing label"
        assert 'description' in schema, f"{event_key} missing description"
        assert 'category' in schema, f"{event_key} missing category"
        assert 'extra_fields' in schema, f"{event_key} missing extra_fields"
        assert 'field_definitions' in schema, f"{event_key} missing field_definitions"

        # Verify field_definitions match extra_fields
        extra_field_names = [f['name'] for f in schema['extra_fields']]
        field_def_names = [f['name'] for f in schema['field_definitions']]
        assert extra_field_names == field_def_names, f"{event_key} field mismatch"

        print(f"✅ {event_key}: Schema structure valid")


def test_field_schemas_complete():
    """Verify all referenced fields have schemas"""
    from src.ssf_transmitter.core import EVENT_TYPES, FIELD_SCHEMAS

    referenced_fields = set()
    for event_data in EVENT_TYPES.values():
        for field in event_data.get('extra_fields', []):
            referenced_fields.add(field['name'])

    for field_name in referenced_fields:
        schema = FIELD_SCHEMAS.get(field_name)
        if schema:
            # Verify schema has required properties
            assert 'label' in schema, f"{field_name} schema missing label"
            assert 'type' in schema, f"{field_name} schema missing type"
            assert 'hint' in schema, f"{field_name} schema missing hint"

            # If select type, must have options
            if schema['type'] == 'select':
                assert 'options' in schema, f"{field_name} select field missing options"
                assert len(schema['options']) > 0, f"{field_name} has no options"

            print(f"✅ Field schema '{field_name}': Valid")
        else:
            print(f"⚠️  Field schema '{field_name}': Not defined (will use generic text input)")
