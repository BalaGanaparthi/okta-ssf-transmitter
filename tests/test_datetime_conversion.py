"""
Test datetime conversion from UI format to Unix timestamp
"""

import pytest
from datetime import datetime


def test_datetime_to_unix_timestamp():
    """Test conversion from datetime-local format to Unix timestamp"""
    # Simulate UI input
    ui_datetime = "2024-03-29T10:30"

    # Convert (same logic as backend)
    dt = datetime.fromisoformat(ui_datetime)
    unix_timestamp = int(dt.timestamp())

    # Verify
    assert isinstance(unix_timestamp, int), "Should be integer"
    assert unix_timestamp > 0, "Should be positive"

    # Verify reverse conversion
    dt_back = datetime.fromtimestamp(unix_timestamp)
    assert dt_back.year == 2024
    assert dt_back.month == 3
    assert dt_back.day == 29
    assert dt_back.hour == 10
    assert dt_back.minute == 30

    print(f"✅ Datetime conversion: {ui_datetime} → {unix_timestamp}")


def test_credential_compromise_with_timestamp(jwt_handler):
    """Test CREDENTIAL_COMPROMISE with event_timestamp conversion"""
    from src.ssf_transmitter.core import get_event_uri
    import jwt as pyjwt

    # Simulate datetime conversion (as backend does)
    ui_datetime = "2024-03-29T15:45"
    dt = datetime.fromisoformat(ui_datetime)
    unix_timestamp = int(dt.timestamp())

    # Extra fields with converted timestamp
    extra_fields = {
        'credential_type': 'password',
        'event_timestamp': unix_timestamp  # Already converted
    }

    # Generate JWT
    event_uri = get_event_uri('CREDENTIAL_COMPROMISE')
    token = jwt_handler.generate_set(
        event_uri,
        'test@example.com',
        'Breach detected',
        extra_fields
    )

    # Decode and verify
    decoded = pyjwt.decode(token, options={"verify_signature": False})
    event_data = decoded['events'][event_uri]

    # Verify timestamp is in JWT as Unix timestamp
    assert 'event_timestamp' in event_data
    assert isinstance(event_data['event_timestamp'], int)
    assert event_data['event_timestamp'] == unix_timestamp

    print(f"✅ CREDENTIAL_COMPROMISE with timestamp: {ui_datetime} → {unix_timestamp}")
    print(f"   event_timestamp in JWT: {event_data['event_timestamp']}")


def test_various_datetime_formats():
    """Test various datetime inputs"""
    test_cases = [
        "2024-01-15T09:00",
        "2024-12-31T23:59",
        "2024-06-15T12:30",
    ]

    for ui_datetime in test_cases:
        dt = datetime.fromisoformat(ui_datetime)
        unix_timestamp = int(dt.timestamp())

        # Verify conversion
        assert unix_timestamp > 0
        dt_back = datetime.fromtimestamp(unix_timestamp)
        assert dt_back.year == dt.year
        assert dt_back.month == dt.month
        assert dt_back.day == dt.day
        assert dt_back.hour == dt.hour
        assert dt_back.minute == dt.minute

        print(f"✅ {ui_datetime} → {unix_timestamp}")


def test_current_time_default():
    """Test that current time can be used as default"""
    import time

    # Get current time as Unix timestamp
    current_unix = int(time.time())

    # Simulate UI getting current time
    now = datetime.now()
    ui_datetime = now.strftime("%Y-%m-%dT%H:%M")

    # Convert
    dt = datetime.fromisoformat(ui_datetime)
    converted_unix = int(dt.timestamp())

    # Should be within a few seconds of current time
    assert abs(converted_unix - current_unix) < 60, "Conversion should be close to current time"

    print(f"✅ Current time conversion works")
    print(f"   UI format: {ui_datetime}")
    print(f"   Unix timestamp: {converted_unix}")
