"""Validation utilities for WhatsApp messages."""
from typing import Dict, Any
from src.utils.logger import setup_logger
from src.config.whatsapp import DEBUG_PHONE_NUMBER

logger = setup_logger(__name__)

def validate_sender(message: Dict[str, Any]) -> bool:
    """
    Validate if the message should be processed based on sender criteria.
    
    Args:
        message (Dict[str, Any]): The incoming WhatsApp message
        
    Returns:
        bool: True if message should be processed, False otherwise
    """
    # If it's our own message or a message status update, ignore it
    if message.get('from_me') or message.get('event', {}).get('type') == 'statuses':
        logger.debug("Ignoring own message or status update")
        return False
        
    # For incoming messages, validate the sender
    sender_number = message.get('from', '').strip()
    logger.debug("Received message from number: %s", sender_number)

    if sender_number != DEBUG_PHONE_NUMBER:
        logger.debug("Skipping message from %s - not the debug number", sender_number)
        return False

    return True