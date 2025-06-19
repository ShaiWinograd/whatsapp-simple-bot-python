"""Core message processing logic for WhatsApp bot."""
from src.config.responses import RESPONSES, DEBUG_PHONE_NUMBER
from src.utils.validators import validate_sender
from webhook_payload import TextMessagePayload

def handle_text_message(message, base_payload):
    """
    Handle text message type and return appropriate response.
    
    Args:
        message (dict): The incoming WhatsApp message
        base_payload (dict): Base payload for response message
        
    Returns:
        dict: Message payload to send or None if no response needed
    """
    command_text = message.get('text', {}).get('body', '').strip().lower()
    
    if command_text == 'היי אמא':
        return TextMessagePayload(
            to=base_payload["to"],
            body=RESPONSES['היי אמא']
        ).to_dict()
    
    print(f"Unknown command received: {command_text}. No response sent.\n")
    return None

def process_message(message):
    """
    Process incoming WhatsApp message and return appropriate response payload.
    
    Args:
        message (dict): The incoming WhatsApp message
        
    Returns:
        dict: Message payload to send or None if no response needed
    """
    if not validate_sender(message):
        return None

    # Create a base payload object for the specific number we're testing with
    base_payload = {
        "to": DEBUG_PHONE_NUMBER,
    }

    command_type = message.get('type', '').strip().lower()
    print(f"Received message type: {command_type}\n")
    
    if command_type == 'text':
        return handle_text_message(message, base_payload)

    return None