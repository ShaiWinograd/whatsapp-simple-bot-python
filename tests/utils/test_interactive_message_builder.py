"""Tests for interactive message builder."""
import pytest
from src.utils.interactive_message_builder import create_interactive_message
from src.config.responses.common import GENERAL

def test_create_interactive_message_default():
    """Test creating interactive message with default values."""
    recipient = "1234567890"
    result = create_interactive_message(recipient)
    
    # Check base structure
    assert result["messaging_product"] == "whatsapp"
    assert result["recipient_type"] == "individual"
    assert result["to"] == recipient
    
    # Check body contains default welcome message
    expected_body = f"{GENERAL['intro']}\n\n{GENERAL['welcome_message']}"
    assert result["text"]["body"] == expected_body
    
    # Check header is default
    assert result["header"]["text"] == GENERAL['header']
    
    # Check action and buttons
    assert result["action"]["type"] == "button"
    buttons = result["action"]["buttons"]
    assert len(buttons) == len(GENERAL['options'])
    for i, button in enumerate(buttons):
        assert button["type"] == "quick_reply"
        assert button["id"] == str(i)
        assert button["title"] == GENERAL['options'][i]

def test_create_interactive_message_custom():
    """Test creating interactive message with custom values."""
    recipient = "1234567890"
    body_text = "Custom body"
    header_text = "Custom header"
    footer_text = "Custom footer"
    buttons = [
        {"id": "custom1", "title": "Button 1"},
        {"id": "custom2", "title": "Button 2"}
    ]
    
    result = create_interactive_message(
        recipient=recipient,
        body_text=body_text,
        header_text=header_text,
        footer_text=footer_text,
        buttons=buttons
    )
    
    # Check base structure
    assert result["messaging_product"] == "whatsapp"
    assert result["recipient_type"] == "individual"
    assert result["to"] == recipient
    
    # Check message components
    assert result["text"]["body"] == body_text
    assert result["header"]["text"] == header_text
    assert result["footer"]["text"] == footer_text
    
    # Check action and buttons
    assert result["action"]["type"] == "button"
    result_buttons = result["action"]["buttons"]
    assert len(result_buttons) == len(buttons)
    for i, button in enumerate(result_buttons):
        assert button["type"] == "quick_reply"
        assert button["id"] == buttons[i]["id"]
        assert button["title"] == buttons[i]["title"]

def test_create_interactive_message_minimal():
    """Test creating interactive message with minimal required fields."""
    recipient = "1234567890"
    body_text = "Test body"
    buttons = [{"id": "1", "title": "Button 1"}]
    
    result = create_interactive_message(
        recipient=recipient,
        body_text=body_text,
        buttons=buttons
    )
    
    # Check required fields
    assert result["messaging_product"] == "whatsapp"
    assert result["recipient_type"] == "individual"
    assert result["to"] == recipient
    assert result["text"]["body"] == body_text
    assert result["action"]["type"] == "button"
    assert result["action"]["buttons"] == [{"type": "quick_reply", "id": "1", "title": "Button 1"}]
    
    # Check optional fields are not present
    assert "header" not in result
    assert "footer" not in result