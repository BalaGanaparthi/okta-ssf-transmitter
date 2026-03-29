"""
Core module tests
"""

import pytest
from src.ssf_transmitter.core import EVENT_TYPES, get_event_type, validate_event_type


def test_event_types_defined():
    """Test that event types are properly defined"""
    # 6 events supported by Okta
    assert 'DEVICE_RISK_CHANGE' in EVENT_TYPES
    assert 'IP_CHANGE' in EVENT_TYPES
    assert 'USER_RISK_CHANGE' in EVENT_TYPES
    assert 'DEVICE_COMPLIANCE_CHANGE' in EVENT_TYPES
    assert 'SESSION_REVOKED' in EVENT_TYPES
    assert 'IDENTIFIER_CHANGED' in EVENT_TYPES
    assert len(EVENT_TYPES) == 6


def test_get_event_type():
    """Test getting event type by key"""
    event = get_event_type('USER_RISK_CHANGE')
    assert event is not None
    assert 'uri' in event
    assert 'label' in event
    assert 'description' in event


def test_validate_event_type():
    """Test event type validation"""
    assert validate_event_type('USER_RISK_CHANGE') is True
    assert validate_event_type('IDENTIFIER_CHANGED') is True
    assert validate_event_type('INVALID_TYPE') is False


def test_jwt_handler_generate_set(jwt_handler):
    """Test SET generation"""
    token = jwt_handler.generate_set(
        'https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required',
        'test@example.com',
        'Test reason'
    )
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_key_manager_generate_keys(temp_keys):
    """Test key generation"""
    assert temp_keys.private_key_path.exists()
    assert temp_keys.public_key_path.exists()


def test_key_manager_get_jwks(temp_keys):
    """Test JWKS generation"""
    jwks = temp_keys.get_jwks('test-key-1')
    assert 'keys' in jwks
    assert len(jwks['keys']) == 1
    assert jwks['keys'][0]['kid'] == 'test-key-1'
