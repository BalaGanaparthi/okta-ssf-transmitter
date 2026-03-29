"""
Core module tests
"""

import pytest
from src.ssf_transmitter.core import EVENT_TYPES, get_event_type, validate_event_type


def test_event_types_defined():
    """Test that event types are properly defined"""
    assert 'CREDENTIAL_CHANGE_REQUIRED' in EVENT_TYPES
    assert 'ACCOUNT_DISABLED' in EVENT_TYPES
    assert 'ACCOUNT_ENABLED' in EVENT_TYPES


def test_get_event_type():
    """Test getting event type by key"""
    event = get_event_type('CREDENTIAL_CHANGE_REQUIRED')
    assert event is not None
    assert 'uri' in event
    assert 'label' in event
    assert 'description' in event


def test_validate_event_type():
    """Test event type validation"""
    assert validate_event_type('CREDENTIAL_CHANGE_REQUIRED') is True
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
