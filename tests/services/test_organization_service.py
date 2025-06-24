"""Tests for the OrganizationService class."""
import pytest
from src.services.organization_service import OrganizationService
from src.config.responses import SERVICE_RESPONSES, GENERAL


@pytest.fixture
def organization_service():
    """Fixture for creating an OrganizationService instance."""
    return OrganizationService(recipient="1234567890")


def test_initialization(organization_service):
    """Test OrganizationService initialization."""
    assert organization_service.recipient == "1234567890"
    assert organization_service.get_conversation_state() == "initial"
    assert organization_service.customer_details is None
    assert organization_service.responses == SERVICE_RESPONSES['organization']


def test_get_service_name(organization_service):
    """Test get_service_name returns correct value."""
    assert organization_service.get_service_name() == SERVICE_RESPONSES['organization']['service_name']


def test_handle_initial_message(organization_service, mocker):
    """Test handle_initial_message sets correct state and returns proper message."""
    # Mock the _apply_service_label method
    mocker.patch.object(organization_service, '_apply_service_label')
    
    messages = organization_service.handle_initial_message()
    
    # Verify state change
    assert organization_service.get_conversation_state() == "awaiting_customer_details"
    
    # Verify message structure
    assert len(messages) == 1
    assert 'interactive' in messages[0]
    assert 'body' in messages[0]['interactive']
    
    # Verify service label was applied
    organization_service._apply_service_label.assert_called_once_with('organization')


def test_handle_customer_details_invalid(organization_service):
    """Test handling invalid customer details."""
    organization_service.set_conversation_state("awaiting_customer_details")
    
    # Test empty message
    messages = organization_service._handle_customer_details({"text": {"body": ""}})
    assert len(messages) == 1
    
    # Test too short message
    messages = organization_service._handle_customer_details({"text": {"body": "short"}})
    assert len(messages) == 2
    assert "לא מספיקים" in messages[0]['text']['body']


def test_handle_customer_details_valid(organization_service):
    """Test handling valid customer details."""
    organization_service.set_conversation_state("awaiting_customer_details")
    
    # Test valid details
    valid_details = "שם: ישראל ישראלי, טלפון: 0501234567, כתובת: תל אביב"
    messages = organization_service._handle_customer_details({"text": {"body": valid_details}})
    
    assert len(messages) == 1
    assert organization_service.customer_details == valid_details
    assert organization_service.get_conversation_state() == "awaiting_verification"


def test_handle_verification_confirmed(organization_service):
    """Test handling verification confirmation."""
    organization_service.set_conversation_state("awaiting_verification")
    organization_service.customer_details = "Test details"
    
    messages = organization_service._handle_verification({
        "interactive": {"button_reply": {"title": "כן, הפרטים נכונים"}}
    })
    
    assert len(messages) == 1
    assert 'interactive' in messages[0]


def test_handle_verification_correction(organization_service):
    """Test handling verification correction request."""
    organization_service.set_conversation_state("awaiting_verification")
    organization_service.customer_details = "Test details"
    
    messages = organization_service._handle_verification({
        "interactive": {"button_reply": {"title": "לא, צריך לתקן"}}
    })
    
    assert len(messages) == 1
    assert organization_service.customer_details is None
    assert organization_service.get_conversation_state() == "awaiting_customer_details"


def test_handle_invalid_state(organization_service):
    """Test handling invalid state."""
    organization_service.set_conversation_state("invalid_state")
    
    messages = organization_service.handle_response({"text": {"body": "test"}})
    
    assert len(messages) == 1
    assert organization_service.get_conversation_state() == "awaiting_customer_details"


def test_handle_response_error(organization_service):
    """Test handling response with error."""
    organization_service.set_conversation_state("awaiting_verification")
    
    # Test with invalid message format
    messages = organization_service.handle_response({})
    
    assert len(messages) == 1
    assert messages[0]['text']['body'] == GENERAL['error']