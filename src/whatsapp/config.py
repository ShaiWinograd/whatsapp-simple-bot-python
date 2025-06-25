"""WhatsApp API configuration module.

This module contains all WhatsApp-specific configuration including:
- API endpoints and authentication
- Label mappings
- Message type definitions
"""
from typing import TypedDict, Dict
import os

# Type definitions for better type safety
class APIEndpoints(TypedDict):
    text: str
    interactive: str
    labels: str

class APIConfig(TypedDict):
    base_url: str
    endpoints: APIEndpoints
    headers: Dict[str, str]

class WhatsAppLabels(TypedDict):
    bot_new_conversation: str
    waiting_urgent_support: str
    waiting_call_before_quote: str
    moving: str
    organization: str

# WhatsApp API configuration
API: APIConfig = {
    'base_url': os.getenv('API_URL', ''),
    'endpoints': {
        'text': 'messages/text',
        'interactive': 'messages/interactive',
        'labels': 'messages/labels'
    },
    'headers': {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': f"Bearer {os.getenv('TOKEN', '')}"
    }
}

# WhatsApp Label IDs with type safety
LABELS: WhatsAppLabels = {
    'bot_new_conversation': os.getenv('WHATSAPP_BOT_NEW_CONVERSATION_LABEL_ID', ''),
    'waiting_urgent_support': os.getenv('WHATSAPP_URGENT_SUPPORT_LABEL_ID', ''),
    'waiting_call_before_quote': os.getenv('WHATSAPP_WAITING_CALL_BEFORE_QUOTE_LABEL_ID', ''),
    'moving': os.getenv('WHATSAPP_MOVING_LABEL_ID', ''),
    'organization': os.getenv('WHATSAPP_ORGANIZATION_LABEL_ID', ''),
}

def get_api_url(message_type: str) -> str:
    """Get the appropriate API URL based on message type.
    
    Args:
        message_type: The type of message (text, interactive, labels)
        
    Returns:
        Complete API URL for the specified message type
    """
    endpoint = API['endpoints'].get(message_type, 'text')
    return f"{API['base_url']}{endpoint}"

# Debug phone number from environment
DEBUG_PHONE_NUMBER: str = os.getenv('DEBUG_PHONE_NUMBER', '')

def is_debug_number(phone_number: str) -> bool:
    """Check if a phone number is the debug phone number.
    
    Args:
        phone_number: The phone number to check
        
    Returns:
        True if number matches debug number when set
    """
    if not DEBUG_PHONE_NUMBER:
        return True
    return phone_number == DEBUG_PHONE_NUMBER