"""Common test fixtures and configurations."""
import pytest
from unittest.mock import Mock
from src.utils.whatsapp_client import WhatsAppClient


@pytest.fixture(autouse=True)
def mock_whatsapp_client(monkeypatch):
    """Mock WhatsAppClient methods for all tests."""
    mock_client = Mock(spec=WhatsAppClient)
    
    # Mock static methods
    monkeypatch.setattr(WhatsAppClient, 'send_message', mock_client.send_message)
    monkeypatch.setattr(WhatsAppClient, 'apply_label', mock_client.apply_label)
    monkeypatch.setattr(WhatsAppClient, 'remove_label', mock_client.remove_label)
    
    return mock_client


@pytest.fixture
def mock_message_text():
    """Fixture for text message payload."""
    return {
        "text": {
            "body": "Test message"
        }
    }


@pytest.fixture
def mock_message_interactive():
    """Fixture for interactive message payload."""
    return {
        "interactive": {
            "button_reply": {
                "id": "test_button",
                "title": "Test Button"
            }
        }
    }


@pytest.fixture
def mock_customer_details():
    """Fixture for customer details."""
    return "שם: ישראל ישראלי\nטלפון: 0501234567\nכתובת: רחוב הרצל 1, תל אביב"


@pytest.fixture
def mock_response_config():
    """Fixture for response configuration."""
    return {
        'header': 'Test Header',
        'body': 'Test Body',
        'footer': 'Test Footer',
        'buttons': [
            {'id': '1', 'title': 'Button 1'},
            {'id': '2', 'title': 'Button 2'}
        ]
    }


@pytest.fixture
def mock_available_slots():
    """Fixture for available time slots."""
    return [
        {'id': 'slot_1', 'title': '10:00-11:00'},
        {'id': 'slot_2', 'title': '11:00-12:00'},
        {'id': 'slot_3', 'title': '12:00-13:00'}
    ]


@pytest.fixture
def mock_service_responses():
    """Fixture for service responses configuration."""
    return {
        'service_name': 'Test Service',
        'rewrite_details': {
            'header': 'Details Header',
            'body': 'Please provide your details',
            'footer': 'Details Footer',
            'buttons': ['Continue']
        },
        'verify_details': {
            'message': 'Verify these details: {details}',
            'options': {
                'buttons': ['כן, הפרטים נכונים', 'לא, צריך לתקן']
            }
        },
        'verify': {
            'header': 'Verification',
            'footer': 'Please confirm'
        },
        'completed': {
            'after_media': 'Thank you for providing your details'
        },
        'scheduling': {
            'header': 'Schedule Header',
            'footer': 'Schedule Footer'
        },
        'fallback': {
            'body': 'Something went wrong',
            'header': 'Error',
            'footer': 'Please try again'
        }
    }