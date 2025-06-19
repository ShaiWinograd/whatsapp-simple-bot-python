"""Configuration for message responses"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define responses for specific commands
RESPONSES = {
    'היי אמא': 'תפסיקי לשגע אותי',
}

# WhatsApp API configuration
WHATSAPP_API = {
    'url': f"{os.getenv('API_URL')}messages/text",
    'headers': {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': f"Bearer {os.getenv('TOKEN')}"
    }
}

# Debug phone number
DEBUG_PHONE_NUMBER = "972546626125" # Shai