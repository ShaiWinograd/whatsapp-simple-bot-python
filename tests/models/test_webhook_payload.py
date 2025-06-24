"""Tests for webhook payload models."""
import pytest
from src.models.webhook_payload import (
    BaseWebhookPayload,
    TextMessagePayload,
    InteractiveMessagePayload
)

def test_base_webhook_payload():
    """Test base webhook payload creation."""
    payload = BaseWebhookPayload(to="1234567890")
    result = payload.to_dict()
    
    assert result["messaging_product"] == "whatsapp"
    assert result["recipient_type"] == "individual"
    assert result["to"] == "1234567890"

def test_text_message_payload():
    """Test text message payload creation."""
    payload = TextMessagePayload(to="1234567890", body="Test message")
    result = payload.to_dict()
    
    assert result["body"]["text"] == "Test message"

def test_interactive_message_payload():
    """Test interactive message payload creation with all fields."""
    buttons = [
        {"id": "1", "title": "Button 1"},
        {"id": "2", "title": "Button 2"}
    ]
    
    payload = InteractiveMessagePayload(
        to="1234567890",
        body_text="Test body",
        header_text="Test header",
        footer_text="Test footer",
        buttons=buttons
    )
    
    result = payload.to_dict()
    
    # Check main structure
    assert result["messaging_product"] == "whatsapp"
    assert result["recipient_type"] == "individual"
    assert result["to"] == "1234567890"
    
    # Check message components
    assert result["body"]["text"] == "Test body"
    assert result["header"]["text"] == "Test header"
    assert result["footer"]["text"] == "Test footer"
    
    # Check buttons
    assert "action" in result
    buttons = result["action"]["buttons"]
    assert len(buttons) == 2
    assert all(b["type"] == "quick_reply" for b in buttons)
    assert buttons[0] == {"type": "quick_reply", "id": "1", "title": "Button 1"}
    assert buttons[1] == {"type": "quick_reply", "id": "2", "title": "Button 2"}

def test_interactive_message_payload_minimal():
    """Test interactive message payload with only required fields."""
    buttons = [{"id": "1", "title": "Button 1"}]
    payload = InteractiveMessagePayload(
        to="1234567890",
        body_text="Test body",
        buttons=buttons
    )
    
    result = payload.to_dict()
    
    # Check required fields
    assert result["body"]["text"] == "Test body"
    assert result["action"]["buttons"] == [{"type": "quick_reply", "id": "1", "title": "Button 1"}]
    
    # Check optional fields are not present
    assert "header" not in result
    assert "footer" not in result