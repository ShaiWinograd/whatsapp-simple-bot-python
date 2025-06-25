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
        print("\n=== WhatsAppClient.send_message() ===")
        print(f"Incoming payload: {payload}")

        # Determine message type from payload structure
        message_type = 'text'
        if payload.get('type') == 'button':
            message_type = 'interactive'
        print(f"Determined message type: {message_type}")
        
        if message_type == 'interactive':
            print("Validating interactive message payload...")
            required_fields = ['messaging_product', 'to', 'type', 'body', 'action']
            if not all(key in payload for key in required_fields):
                missing = [f for f in required_fields if f not in payload]
                print(f"Missing required fields: {missing}")
                raise ValueError(f"Interactive messages must have these fields: {', '.join(required_fields)}")
            
            if 'text' not in payload['body']:
                print("Error: 'text' field missing in body")
                raise ValueError("Interactive message body must have 'text' field")
                
            if 'buttons' not in payload['action']:
                print("Error: 'buttons' field missing in action")
                raise ValueError("Interactive message action must have 'buttons' field")
            
            print("Interactive message validation passed")
        else:
            print("Validating text message payload...")
            # For text messages, validate required fields
            required_fields = ['messaging_product', 'to', 'body']
            if not all(key in payload for key in required_fields):
                missing = [f for f in required_fields if f not in payload]
                print(f"Missing required fields: {missing}")
                raise ValueError(f"Text messages must have these fields: {', '.join(required_fields)}")
            
            # For text messages, body must be a string
            if not isinstance(payload['body'], str):
                print(f"Error: body is type {type(payload['body'])}, expected str")
                print(f"Body content: {payload['body']}")
                raise ValueError("Text message body must be a string")
            
            print("Text message validation passed")
            
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