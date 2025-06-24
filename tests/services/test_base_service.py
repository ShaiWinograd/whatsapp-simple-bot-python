"""Tests for the BaseConversationService class."""
import pytest
from src.services.base_service import BaseConversationService
from src.config.responses.common import NAVIGATION, GENERAL
from src.utils.whatsapp_client import WhatsAppClient


class TestService(BaseConversationService):
    """Test implementation of BaseConversationService."""
    
    def get_service_name(self) -> str:
        return "test_service"
        
    def handle_initial_message(self):
        return [self.create_text_message("initial")]
        
    def handle_response(self, message):
        return [self.create_text_message("response")]


@pytest.fixture
def base_service():
    """Fixture for creating a TestService instance."""
    return TestService(recipient="1234567890")


def test_initialization(base_service):
    """Test BaseConversationService initialization."""
    assert base_service.recipient == "1234567890"
    assert base_service.conversation_state == "initial"
    assert base_service.customer_details is None
    assert base_service.current_label is None


def test_conversation_state_management(base_service):
    """Test conversation state getters and setters."""
    assert base_service.get_conversation_state() == "initial"
    
    base_service.set_conversation_state("new_state")
    assert base_service.get_conversation_state() == "new_state"


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


def test_handle_slot_selection(base_service):
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


@pytest.mark.asyncio
async def test_apply_service_label(base_service, mocker):
    """Test service label application."""
    # Mock WhatsAppClient methods
    mocker.patch.object(WhatsAppClient, 'apply_label')
    mocker.patch.object(WhatsAppClient, 'remove_label')
    
    # Test applying new label
    base_service._apply_service_label('test_label')
    
    # Verify WhatsAppClient calls
    WhatsAppClient.apply_label.assert_called_once()
    WhatsAppClient.remove_label.assert_not_called()
    
    # Reset mock counts
    WhatsAppClient.apply_label.reset_mock()
    WhatsAppClient.remove_label.reset_mock()
    
    # Test changing label
    base_service._apply_service_label('new_label')
    
    # Verify both remove and apply were called
    WhatsAppClient.remove_label.assert_called_once()
    WhatsAppClient.apply_label.assert_called_once()