"""Tests for the OrganizationService class."""
import pytest
from src.services.organization_service import OrganizationService
from src.config.responses import SERVICE_RESPONSES, GENERAL
from src.chat.conversation_manager import ConversationManager


@pytest.fixture
def mock_conversation_manager(mocker):
    """Fixture for creating a mocked ConversationManager."""
    manager = mocker.Mock(spec=ConversationManager)
    manager.apply_service_label = mocker.Mock()
    return manager


@pytest.fixture
def organization_service(mock_conversation_manager):
    """Fixture for creating an OrganizationService instance with conversation manager."""
    return OrganizationService(recipient="1234567890", conversation_manager=mock_conversation_manager)


@pytest.fixture
def organization_service_no_manager():
    """Fixture for creating an OrganizationService instance without conversation manager."""
    return OrganizationService(recipient="1234567890")


def test_initialization_with_manager(organization_service, mock_conversation_manager):
    """Test OrganizationService initialization with manager."""
    assert organization_service.recipient == "1234567890"
    assert organization_service.get_conversation_state() == "initial"
    assert organization_service.customer_details is None
    assert organization_service.conversation_manager == mock_conversation_manager
    assert organization_service.responses == SERVICE_RESPONSES['organization']


def test_initialization_without_manager(organization_service_no_manager):
    """Test OrganizationService initialization without manager."""
    assert organization_service_no_manager.recipient == "1234567890"
    assert organization_service_no_manager.get_conversation_state() == "initial"
    assert organization_service_no_manager.customer_details is None
    assert organization_service_no_manager.conversation_manager is None
    assert organization_service_no_manager.responses == SERVICE_RESPONSES['organization']


def test_get_service_name(organization_service):
    """Test get_service_name returns correct value."""
    assert organization_service.get_service_name() == SERVICE_RESPONSES['organization']['service_name']


def test_handle_initial_message_with_manager(organization_service, mock_conversation_manager):
    """Test handle_initial_message with conversation manager."""
    messages = organization_service.handle_initial_message()
    
    mock_conversation_manager.update_service_state.assert_called_once_with(
        "1234567890", "awaiting_customer_details"
    )
    assert len(messages) == 1
    assert 'body' in messages[0]
    assert 'action' in messages[0]
    assert 'buttons' in messages[0]['action']


def test_handle_initial_message_without_manager(organization_service_no_manager):
    """Test handle_initial_message without conversation manager."""
    messages = organization_service_no_manager.handle_initial_message()
    
    assert organization_service_no_manager.get_conversation_state() == "awaiting_customer_details"
    assert len(messages) == 1
    assert 'body' in messages[0]
    assert 'action' in messages[0]
    assert 'buttons' in messages[0]['action']


def test_handle_customer_details_invalid(organization_service):
    """Test handling invalid customer details."""
    # Test empty message
    messages = organization_service._handle_customer_details({"text": {"body": ""}})
    assert len(messages) == 1
    
    # Test too short message
    messages = organization_service._handle_customer_details({"text": {"body": "short"}})
    assert len(messages) == 2
    assert "לא מספיקים" in messages[0]['body']['text']


def test_handle_customer_details_valid_with_manager(organization_service, mock_conversation_manager):
    """Test handling valid customer details with conversation manager."""
    valid_details = "שם: ישראל ישראלי, טלפון: 0501234567, כתובת: תל אביב"
    messages = organization_service._handle_customer_details({"text": {"body": valid_details}})
    
    assert len(messages) == 1
    assert organization_service.customer_details == valid_details
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_verification"
    )


def test_handle_customer_details_valid_without_manager(organization_service_no_manager):
    """Test handling valid customer details without conversation manager."""
    valid_details = "שם: ישראל ישראלי, טלפון: 0501234567, כתובת: תל אביב"
    messages = organization_service_no_manager._handle_customer_details({"text": {"body": valid_details}})
    
    assert len(messages) == 1
    assert organization_service_no_manager.customer_details == valid_details
    assert organization_service_no_manager.get_conversation_state() == "awaiting_verification"


def test_handle_verification_confirmed_with_manager(organization_service, mock_conversation_manager):
    """Test handling verification confirmation with conversation manager."""
    organization_service.customer_details = "Test details"
    
    messages = organization_service._handle_verification({
        "interactive": {"button_reply": {"title": "כן, הפרטים נכונים"}}
    })
    
    assert len(messages) == 1
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "completed"
    )


def test_handle_verification_confirmed_without_manager(organization_service_no_manager):
    """Test handling verification confirmation without conversation manager."""
    organization_service_no_manager.customer_details = "Test details"
    
    messages = organization_service_no_manager._handle_verification({
        "interactive": {"button_reply": {"title": "כן, הפרטים נכונים"}}
    })
    
    assert len(messages) == 1
    assert organization_service_no_manager.get_conversation_state() == "awaiting_slot_selection"


def test_handle_verification_correction(organization_service, mock_conversation_manager):
    """Test handling verification correction request."""
    organization_service.customer_details = "Test details"
    
    messages = organization_service._handle_verification({
        "interactive": {"button_reply": {"title": "לא, צריך לתקן"}}
    })
    
    assert len(messages) == 1
    assert organization_service.customer_details is None
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_customer_details"
    )


def test_handle_invalid_state_with_manager(organization_service, mock_conversation_manager):
    """Test handling invalid state with conversation manager."""
    organization_service.set_conversation_state("invalid_state")
    
    messages = organization_service.handle_response({"text": {"body": "test"}})
    
    assert len(messages) == 1
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_customer_details"
    )


def test_handle_invalid_state_without_manager(organization_service_no_manager):
    """Test handling invalid state without conversation manager."""
    organization_service_no_manager.set_conversation_state("invalid_state")
    
    messages = organization_service_no_manager.handle_response({"text": {"body": "test"}})
    
    assert len(messages) == 1
    assert organization_service_no_manager.get_conversation_state() == "awaiting_customer_details"


def test_handle_response_error(organization_service):
    """Test handling response with error."""
    messages = organization_service.handle_response({})
    
    assert len(messages) == 1
    assert messages[0]['body']['text'] == GENERAL['error']