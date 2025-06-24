"""Tests for interactive message handler."""
import pytest
from unittest.mock import Mock, patch
from src.chat.handlers.interactive_handler import InteractiveMessageHandler
from src.services.service_factory import ServiceType
from src.utils.errors import ConversationError

@pytest.fixture
def conversation_manager():
    return Mock()

@pytest.fixture
def service_factory():
    return Mock()

@pytest.fixture
def handler(conversation_manager, service_factory):
    handler = InteractiveMessageHandler(conversation_manager, service_factory)
    # Mock the check_existing_conversation method
    handler.check_existing_conversation = Mock(return_value=None)
    return handler

def test_handle_non_interactive_message_new_conversation(handler):
    """Test handling non-interactive message with no existing conversation."""
    message = {"type": "text"}
    base_payload = {"to": "1234567890"}
    
    # check_existing_conversation is already mocked in the fixture
    
    result = handler.handle(message, base_payload)
    
    # Should return welcome message
    assert len(result) == 1
    welcome_payload = result[0]
    assert welcome_payload["type"] == "button"
    assert welcome_payload["to"] == "1234567890"
    assert "text" in welcome_payload
    assert "buttons" in welcome_payload

def test_handle_button_click_main_menu(handler, service_factory):
    """Test handling button click for main menu option."""
    message = {
        "type": "interactive",
        "interactive": {
            "button_reply": {
                "title": "מעבר דירה"
            }
        }
    }
    base_payload = {"to": "1234567890"}
    
    # Mock service creation
    mock_service = Mock()
    mock_service.handle_initial_message.return_value = [{"type": "text", "text": {"body": "Service response"}}]
    service_factory.create.return_value = mock_service
    
    result = handler.handle(message, base_payload)
    
    # Verify service was created with correct type
    service_factory.create.assert_called_once_with(
        ServiceType.MOVING,
        "1234567890",
        handler.conversation_manager
    )
    
    # Verify conversation was added
    handler.conversation_manager.add_conversation.assert_called_once_with(
        "1234567890",
        mock_service
    )
    
    # Verify service response was returned
    assert len(result) == 1
    assert result[0]["text"]["body"] == "Service response"

def test_handle_back_to_main_menu(handler):
    """Test handling 'back to main menu' button click."""
    message = {
        "type": "interactive",
        "interactive": {
            "button_reply": {
                "title": "חזרה לתפריט הראשי"
            }
        }
    }
    base_payload = {"to": "1234567890"}
    
    result = handler.handle(message, base_payload)
    
    # Verify conversation was removed
    handler.conversation_manager.remove_conversation.assert_called_once_with("1234567890")
    
    # Verify welcome message was returned
    assert len(result) == 1
    welcome_payload = result[0]
    assert welcome_payload["type"] == "button"
    assert welcome_payload["to"] == "1234567890"
    assert "text" in welcome_payload
    assert "buttons" in welcome_payload

def test_handle_human_support_request(handler, service_factory):
    """Test handling request for human support."""
    message = {
        "type": "interactive",
        "interactive": {
            "button_reply": {
                "title": "אשמח לדבר עם נציג/ה"
            }
        }
    }
    base_payload = {"to": "1234567890"}
    
    # Mock human support service
    mock_service = Mock()
    mock_service.handle_initial_message.return_value = [{"type": "text", "text": {"body": "Human support response"}}]
    service_factory.create.return_value = mock_service
    
    result = handler.handle(message, base_payload)
    
    # Verify correct service was created
    service_factory.create.assert_called_once_with(
        ServiceType.HUMAN_SUPPORT,
        "1234567890",
        handler.conversation_manager
    )
    
    # Verify conversation was added
    handler.conversation_manager.add_conversation.assert_called_once_with(
        "1234567890",
        mock_service
    )
    
    # Verify service response was returned
    assert len(result) == 1
    assert result[0]["text"]["body"] == "Human support response"

def test_handle_service_creation_error(handler, service_factory):
    """Test handling error during service creation."""
    message = {
        "type": "interactive",
        "interactive": {
            "button_reply": {
                "title": "מעבר דירה"
            }
        }
    }
    base_payload = {"to": "1234567890"}
    
    # Mock service creation to raise error
    service_factory.create.side_effect = ConversationError("Test error")
    
    result = handler.handle(message, base_payload)
    
    # Should return to welcome message on error
    assert len(result) == 1
    welcome_payload = result[0]
    assert welcome_payload["type"] == "button"
    assert welcome_payload["to"] == "1234567890"
    assert "text" in welcome_payload
    assert "buttons" in welcome_payload