"""Tests for the BaseConversationService class."""
import pytest
from src.services.base_service import BaseConversationService
from src.config.responses.common import NAVIGATION, GENERAL
from src.chat.conversation_manager import ConversationManager


class TestService(BaseConversationService):
    """Test implementation of BaseConversationService."""
    
    def get_service_name(self) -> str:
        return "test_service"
        
    def handle_initial_message(self):
        return [self.create_text_message("initial")]
        
    def handle_response(self, message):
        return [self.create_text_message("response")]


@pytest.fixture
def mock_conversation_manager(mocker):
    """Fixture for creating a mocked ConversationManager."""
    manager = mocker.Mock(spec=ConversationManager)
    return manager


@pytest.fixture
def base_service(mock_conversation_manager):
    """Fixture for creating a TestService instance with conversation manager."""
    return TestService(recipient="1234567890", conversation_manager=mock_conversation_manager)


@pytest.fixture
def base_service_no_manager():
    """Fixture for creating a TestService instance without conversation manager."""
    return TestService(recipient="1234567890")


def test_initialization_with_manager(base_service, mock_conversation_manager):
    """Test BaseConversationService initialization with conversation manager."""
    assert base_service.recipient == "1234567890"
    assert base_service.conversation_state == "initial"
    assert base_service.customer_details is None
    assert base_service.conversation_manager == mock_conversation_manager


def test_initialization_without_manager(base_service_no_manager):
    """Test BaseConversationService initialization without conversation manager."""
    assert base_service_no_manager.recipient == "1234567890"
    assert base_service_no_manager.conversation_state == "initial"
    assert base_service_no_manager.customer_details is None
    assert base_service_no_manager.conversation_manager is None


def test_conversation_state_with_manager(base_service, mock_conversation_manager):
    """Test conversation state management with conversation manager."""
    base_service.set_conversation_state("new_state")
    mock_conversation_manager.update_service_state.assert_called_once_with(
        "1234567890", "new_state"
    )
    assert base_service.get_conversation_state() == "new_state"


def test_conversation_state_without_manager(base_service_no_manager):
    """Test conversation state management without conversation manager."""
    assert base_service_no_manager.get_conversation_state() == "initial"
    
    base_service_no_manager.set_conversation_state("new_state")
    assert base_service_no_manager.get_conversation_state() == "new_state"


def test_create_text_message(base_service):
    """Test text message creation."""
    message = base_service.create_text_message("test message")
    
    assert message['messaging_product'] == "whatsapp"
    assert message['recipient_type'] == "individual"
    assert message['to'] == "1234567890"
    assert message['type'] == "text"
    assert message['text']['body'] == "test message"


def test_create_interactive_message_from_config(base_service):
    """Test interactive message creation from config."""
    config = {
        'body': 'Test body',
        'header': 'Test header',
        'footer': 'Test footer',
        'buttons': ['Button 1', 'Button 2']
    }
    
    message = base_service._create_interactive_message_from_config(config)
    
    assert message['messaging_product'] == "whatsapp"
    assert message['recipient_type'] == "individual"
    assert message['to'] == "1234567890"
    assert message['type'] == "interactive"
    assert message['interactive']['body']['text'] == 'Test body'
    assert message['interactive']['header']['text'] == 'Test header'
    assert message['interactive']['footer']['text'] == 'Test footer'
    assert len(message['interactive']['action']['buttons']) == 2


def test_create_interactive_message_without_body(base_service):
    """Test interactive message creation without required body."""
    config = {
        'header': 'Test header',
        'buttons': ['Button 1']
    }
    
    with pytest.raises(KeyError, match="Required 'body' key missing from config"):
        base_service._create_interactive_message_from_config(config)


def test_create_verification_message(base_service):
    """Test verification message creation."""
    base_service.customer_details = "Test details"
    base_service.responses = {
        'verify_details': {
            'message': 'Details: {details}',
            'options': {
                'buttons': ['Yes', 'No']
            }
        },
        'verify': {
            'header': 'Verify',
            'footer': 'Please confirm'
        }
    }
    
    message = base_service._create_verification_message()
    
    assert message['type'] == "interactive"
    assert 'Test details' in message['interactive']['body']['text']
    assert len(message['interactive']['action']['buttons']) == 2


def test_create_verification_message_without_details(base_service):
    """Test verification message creation without customer details."""
    with pytest.raises(ValueError, match="Customer details must be set"):
        base_service._create_verification_message()


def test_handle_slot_selection(base_service, mock_conversation_manager):
    """Test slot selection handling."""
    # Test back to main menu
    message = {"interactive": {"button_reply": {"title": NAVIGATION['back_to_main']}}}
    response = base_service._handle_slot_selection(message)
    assert len(response) == 1
    assert response[0]['text']['body'] == "initial"
    
    # Test invalid slot
    message = {"interactive": {"button_reply": {"title": ""}}}
    response = base_service._handle_slot_selection(message)
    assert len(response) == 1
    assert response[0]['text']['body'] == GENERAL['error']
    
    # Test valid slot selection
    message = {"interactive": {"button_reply": {"title": "10:00-11:00"}}}
    response = base_service._handle_slot_selection(message)
    assert len(response) == 1
    assert 'interactive' in response[0]


def test_handle_slot_selection_completion(base_service, mock_conversation_manager):
    """Test slot selection completion state handling."""
    slot = "10:00-11:00"
    message = {"interactive": {"button_reply": {"title": slot}}}
    
    response = base_service._handle_slot_selection(message)
    
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_slot_selection"
    )
    assert 'interactive' in response[0]


def test_slot_selection_without_manager(base_service_no_manager):
    """Test slot selection without conversation manager."""
    slot = "10:00-11:00"
    message = {"interactive": {"button_reply": {"title": slot}}}
    
    response = base_service_no_manager._handle_slot_selection(message)
    
    assert base_service_no_manager.get_conversation_state() == "awaiting_slot_selection"
    assert 'interactive' in response[0]