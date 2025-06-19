"""Validation utilities for WhatsApp messages."""
from src.config.responses import DEBUG_PHONE_NUMBER

def validate_sender(message):
    """
    Validate if the message should be processed based on sender criteria.
    
    Args:
        message (dict): The incoming WhatsApp message
        
    Returns:
        bool: True if message should be processed, False otherwise
    """
    # If it's our own message or a message status update, ignore it
    if message.get('from_me') or message.get('event', {}).get('type') == 'statuses':
        return False
        
    # For incoming messages, validate the sender
    sender_number = message.get('from', '').strip()
    print(f"Message from number: {sender_number}\n")

    if sender_number != DEBUG_PHONE_NUMBER:
        print(f"Skipping message from {sender_number} - not the debug number\n")
        return False

    return True