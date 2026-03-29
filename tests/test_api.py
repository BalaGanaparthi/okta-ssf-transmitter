"""
API endpoint tests
"""

import json
import pytest


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_jwks_endpoint(client):
    """Test JWKS endpoint"""
    response = client.get('/.well-known/jwks.json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'keys' in data
    assert len(data['keys']) > 0
    assert data['keys'][0]['kty'] == 'RSA'


def test_config_endpoint(client):
    """Test config endpoint"""
    response = client.get('/api/config')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'issuer' in data
    assert 'oktaDomain' in data
    assert 'keyId' in data


def test_event_types_endpoint(client):
    """Test event types endpoint"""
    response = client.get('/api/event-types')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'CREDENTIAL_CHANGE_REQUIRED' in data
    assert 'ACCOUNT_DISABLED' in data
    assert 'ACCOUNT_ENABLED' in data


def test_send_event_missing_data(client):
    """Test send event with missing data"""
    response = client.post('/api/send-event',
                           data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 400


def test_send_event_invalid_event_type(client):
    """Test send event with invalid event type"""
    response = client.post('/api/send-event',
                           data=json.dumps({
                               'subject': 'test@example.com',
                               'eventType': 'INVALID_TYPE'
                           }),
                           content_type='application/json')
    assert response.status_code == 400


def test_main_page(client):
    """Test main page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'SSF Transmitter' in response.data
