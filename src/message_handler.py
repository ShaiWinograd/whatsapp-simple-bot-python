"""Core message processing logic for WhatsApp bot."""
from typing import List, Dict, Any

from src.config.responses import RESPONSES, DEBUG_PHONE_NUMBER
from src.utils.validators import validate_sender
from webhook_payload import TextMessagePayload, InteractiveMessagePayload

def create_welcome_messages(recipient: str) -> List[Dict[str, Any]]:
    """
    Create welcome and options messages.
    
    Args:
        recipient (str): The recipient's phone number
        
    Returns:
        List[Dict[str, Any]]: List of message payloads to send
    """
    # Create welcome text message
    welcome_message = TextMessagePayload(
        to=recipient,
        body=RESPONSES['welcome_message']
    ).to_dict()
    
    # Create interactive options message
    options_message = InteractiveMessagePayload(
        to=recipient,
        body="אנא בחר/י אחת מהאפשרויות הבאות:",
        button_messages=RESPONSES['options']
    ).to_dict()
    
    return [welcome_message, options_message]

def handle_text_message(message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Handle text message type and return appropriate response.
    
    Args:
        message (dict): The incoming WhatsApp message
        base_payload (dict): Base payload for response message
        
    Returns:
        List[Dict[str, Any]]: List of message payloads to send
    """
    command_text = message.get('text', {}).get('body', '').strip()
    
    if command_text == 'היי אמא':
        return [TextMessagePayload(
            to=base_payload["to"],
            body=RESPONSES['היי אמא']
        ).to_dict()]
    
    # For any other message, send welcome messages
    return create_welcome_messages(base_payload["to"])

def process_message(message: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Process incoming WhatsApp message and return appropriate response payload.
    
    Args:
        message (dict): The incoming WhatsApp message
        
    Returns:
        List[Dict[str, Any]]: List of message payloads to send or empty list if no response needed
    """
    if not validate_sender(message):
        return []

    # Create a base payload object with the sender's number
    base_payload = {
        "to": message.get('from', '').strip(),
    }

    command_type = message.get('type', '').strip().lower()
    print(f"Received message type: {command_type}\n")
    
    if command_type == 'text':
        return handle_text_message(message, base_payload)

    return []