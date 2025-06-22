"""WhatsApp API configuration."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WhatsApp API configuration
API = {
    'base_url': os.getenv('API_URL'),
    'endpoints': {
        'text': 'messages/text',
        'interactive': 'messages/interactive',
        'labels': 'messages/labels'
    },
    'headers': {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': f"Bearer {os.getenv('TOKEN')}"
    }
}

# WhatsApp Label IDs
LABELS = {
    'bot_new_conversation': os.getenv('WHATSAPP_BOT_NEW_CONVERSATION_LABEL_ID', ''),
    'waiting_human_support': os.getenv('WHATSAPP_HUMAN_SUPPORT_LABEL_ID', ''),
    'waiting_quote': os.getenv('WHATSAPP_WAITING_QUOTE_LABEL_ID', ''),
}

# Debug phone number
DEBUG_PHONE_NUMBER = "972546626125"  # Only allow messages from this number

def get_api_url(message_type: str) -> str:
    """Get the appropriate API URL based on message type."""
    endpoint = API['endpoints'].get(message_type, 'text')
    return f"{API['base_url']}{endpoint}"