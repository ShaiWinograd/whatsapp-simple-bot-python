"""Configuration for message responses"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define responses for specific commands
RESPONSES = {
    'welcome_message': 'איזה כיף ששלחת הודעה! איך אפשר לעזור לך היום?',
    'options': [
        'מעבר דירה',
        'סידור וארגון',
        'עיצוב והלבשת הבית',
        'שיחת ייעוץ',
    ],
    'היי אמא': 'את אלופה!',
}

# WhatsApp API configuration
WHATSAPP_API = {
    'base_url': os.getenv('API_URL'),
    'endpoints': {
        'text': 'messages/text',
        'interactive': 'messages/interactive'
    },
    'headers': {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': f"Bearer {os.getenv('TOKEN')}"
    }
}

def get_api_url(message_type: str) -> str:
    """Get the appropriate API URL based on message type."""
    endpoint = WHATSAPP_API['endpoints'].get(message_type, 'text')
    return f"{WHATSAPP_API['base_url']}{endpoint}"

# Debug phone number
DEBUG_PHONE_NUMBER = "972546626125" # Shai