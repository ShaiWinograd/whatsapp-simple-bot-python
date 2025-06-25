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
        # Set required API headers with UTF-8 charset
        self.session.headers.update({
            'Authorization': WHATSAPP_API['headers']['authorization'],
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        })

    def send_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message through the WhatsApp API.
        
        Args:
            payload: Message payload to send. For interactive messages, type should be 'button' by default.
            For text messages, type field should not be present.
            
        Returns:
            API response data
            
        Raises:
            ValueError: If required fields are missing
        """
        # Determine message type and validate payload
        message_type = 'interactive' if 'action' in payload else 'text'
            
        if message_type == 'interactive':
            required_fields = ['messaging_product', 'to', 'type', 'body', 'action']
            if not all(key in payload for key in required_fields):
                raise ValueError(f"Interactive messages must have these fields: {', '.join(required_fields)}")
            
            if 'text' not in payload['body']:
                raise ValueError("Interactive message body must have 'text' field")
                
            if 'buttons' not in payload['action']:
                raise ValueError("Interactive message action must have 'buttons' field")
        else:
            # For text messages, ensure proper structure
            if 'text' not in payload:
                # Convert legacy format to new format
                payload = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": payload.get("to"),
                    "type": "text",
                    "text": {
                        "preview_url": False,
                        "body": payload.get("body", "")
                    }
                }
            
        url = get_api_url(message_type)
        print(f"Sending {message_type} message to {url}")
        
        response = self.session.post(url, json=payload)
        
        # Print response details for debugging
        print(f"Response status: {response.status_code}")
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error response content: {response.text}")
            raise
        response.raise_for_status()
        return response.json()