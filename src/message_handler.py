"""Core message processing logic for WhatsApp bot."""
from typing import List, Dict, Any

from src.config.responses import RESPONSES, DEBUG_PHONE_NUMBER
from src.utils.validators import validate_sender
from src.services import create_service
from webhook_payload import TextMessagePayload, InteractiveMessagePayload


# Store active conversations and their services
active_conversations: Dict[str, Any] = {}


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
        body="מה היית רוצה שנעשה עבורך?",
        button_messages=RESPONSES['options']
    ).to_dict()
    
    return [welcome_message, options_message]


def handle_interactive_message(message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Handle interactive message type and return appropriate response.
    
    Args:
        message (dict): The incoming WhatsApp message
        base_payload (dict): Base payload for response message
        
    Returns:
        List[Dict[str, Any]]: List of message payloads to send
    """
    button_reply = message.get('interactive', {}).get('button_reply', {})
    selected_option = button_reply.get('id', '')
    
    # Check if there's an active conversation for this user
    if base_payload["to"] in active_conversations:
        service = active_conversations[base_payload["to"]]
        return service.handle_response(message)
    
    # If no active conversation, check if this is a service selection
    if selected_option in RESPONSES['options']:
        # Create new service instance
        service = create_service(selected_option, base_payload["to"])
        if service:
            active_conversations[base_payload["to"]] = service
            return service.handle_initial_message()
    
    # If we get here, something went wrong - send welcome messages
    return create_welcome_messages(base_payload["to"])


def handle_text_message(message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Handle text message type and return appropriate response.
    
    Args:
        message (dict): The incoming WhatsApp message
        base_payload (dict): Base payload for response message
        
    Returns:
        List[Dict[str, Any]]: List of message payloads to send
    """
    # Check if there's an active conversation
    if base_payload["to"] in active_conversations:
        service = active_conversations[base_payload["to"]]
        return service.handle_response(message)
    
    # For any other text message, show the welcome message
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

    sender_number = message.get('from', '').strip()
    
    # Check for specific phone number and return custom response
    if sender_number == '972543349144':
        return [TextMessagePayload(
            to=sender_number,
            body="תודה שפנית, אבל שי היא הבת האהובה עלי ואין לי זמן גם אלייך"
        ).to_dict()]

    # Create a base payload object with the sender's number
    base_payload = {
        "to": sender_number,
    }

    command_type = message.get('type', '').strip().lower()
    print(f"Received message type: {command_type}\n")
    
    if command_type == 'text':
        return handle_text_message(message, base_payload)
    elif command_type in ['interactive', 'reply']:
        # For reply type, check if it's a button reply
        if command_type == 'reply' and message.get('reply', {}).get('type') == 'buttons_reply':
            # Extract the actual title from the button reply
            button_title = message.get('reply', {}).get('buttons_reply', {}).get('title', '')
            print(f"Received button reply with title: {button_title}")
            
            if button_title in RESPONSES['options']:
                print(f"Creating service for option: {button_title}")
                service = create_service(button_title, base_payload["to"])
                if service:
                    print(f"Service created successfully")
                    active_conversations[base_payload["to"]] = service
                    return service.handle_initial_message()
                else:
                    print(f"Failed to create service for option: {button_title}")
            else:
                print(f"Button title not found in RESPONSES options: {button_title}")
                
        return handle_interactive_message(message, base_payload)

    print(f"Unhandled message type: {command_type}")
    return []