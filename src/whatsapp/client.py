"""WhatsApp API client implementation."""
import requests
from typing import Any, Dict, Optional
from .config import (
    API as WHATSAPP_API,
    LABELS as WHATSAPP_LABELS,
    get_api_url
)

class WhatsAppClient:
    """Client for interacting with the WhatsApp API."""

    def __init__(self):
        """Initialize the WhatsApp client."""
        self.session = requests.Session()
        self.session.headers.update(WHATSAPP_API['headers'])

    def send_message(self, payload: Dict[str, Any], message_type: str = 'text') -> Dict[str, Any]:
        """Send a message through the WhatsApp API.
        
        Args:
            payload: Message payload to send
            message_type: Type of message (text, interactive, labels)
            
        Returns:
            API response data
        """
        url = get_api_url(message_type)
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()