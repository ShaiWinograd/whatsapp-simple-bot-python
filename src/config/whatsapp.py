"""WhatsApp configuration module.

This module contains WhatsApp-specific configuration for the application including:
- Label mappings
- Debug settings
"""
from typing import TypedDict
import os
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class WhatsAppLabels(TypedDict):
    """WhatsApp label type definitions."""
    bot_new_conversation: str
    waiting_urgent_support: str
    waiting_call_before_quote: str
    moving: str
    organization: str

# WhatsApp Label IDs with type safety
LABELS: WhatsAppLabels = {
    'bot_new_conversation': os.getenv('WHATSAPP_BOT_NEW_CONVERSATION_LABEL_ID', ''),
    'waiting_urgent_support': os.getenv('WHATSAPP_URGENT_SUPPORT_LABEL_ID', ''),
    'waiting_call_before_quote': os.getenv('WHATSAPP_WAITING_CALL_BEFORE_QUOTE_LABEL_ID', ''),
    'moving': os.getenv('WHATSAPP_MOVING_LABEL_ID', ''),
    'organization': os.getenv('WHATSAPP_ORGANIZATION_LABEL_ID', ''),
}

# Debug phone number from environment
DEBUG_PHONE_NUMBER: str = os.getenv('DEBUG_PHONE_NUMBER', '')

if DEBUG_PHONE_NUMBER:
    logger.info("Debug mode enabled - Only processing messages from: %s", DEBUG_PHONE_NUMBER)
else:
    logger.warning("DEBUG_PHONE_NUMBER not set - Processing messages from all numbers")

def is_debug_number(phone_number: str) -> bool:
    """Check if a phone number is the debug phone number.
    
    Args:
        phone_number: The phone number to check
        
    Returns:
        True if DEBUG_PHONE_NUMBER is not set, or if number matches DEBUG_PHONE_NUMBER
    """
    if not DEBUG_PHONE_NUMBER:
        logger.warning("DEBUG_PHONE_NUMBER not set - allowing all numbers")
        return True
        
    normalized_debug = DEBUG_PHONE_NUMBER.strip().replace("+", "")
    normalized_phone = phone_number.strip().replace("+", "")
    match = normalized_phone == normalized_debug
    
    if not match:
        logger.debug("Number %s does not match debug number %s",
                    phone_number, DEBUG_PHONE_NUMBER)
    
    return match

__all__ = ['WhatsAppLabels', 'LABELS', 'DEBUG_PHONE_NUMBER', 'is_debug_number']