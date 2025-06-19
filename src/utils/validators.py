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
    sender_number = message.get('from', '').strip()
    print(f"Message from number: {sender_number}\n")

    # Only process messages from the specific number
    if sender_number != DEBUG_PHONE_NUMBER:
        print(f"Skipping message from {sender_number} - not the debug number\n")
        return False

    # Ignore messages from the bot itself
    if message.get('fromMe'):
        return False

    return True