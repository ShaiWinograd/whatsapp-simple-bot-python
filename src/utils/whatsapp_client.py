"""WhatsApp API client for sending messages."""
import requests
from src.config.responses import WHATSAPP_API, get_api_url

class WhatsAppClient:
    """Client for interacting with WhatsApp API."""
    
    @staticmethod
    def send_message(payload: dict) -> dict:
        """
        Send a message via WhatsApp API.
        
        Args:
            payload (dict): The message payload to send
            
        Returns:
            dict: The API response or error details
        """
        # Determine message type from payload
        message_type = 'interactive' if 'action' in payload else 'text'
        api_url = get_api_url(message_type)
        
        print(f"Sending {message_type} message to URL: {api_url}\n")
        print(f"Payload: {payload}\n")
        
        try:
            response = requests.post(
                api_url,
                json=payload,
                headers=WHATSAPP_API['headers']
            )
            
            print(f"Response status: {response.status_code}\n")
            print(f"Response headers: {response.headers}\n")
            print(f"Response from API: {response.text}\n")
    
            if response.status_code != 200:
                error_msg = {
                    'status_code': response.status_code,
                    'response_text': response.text,
                    'requested_url': api_url,
                    'payload': payload
                }
                print("API Error:", error_msg)
                return error_msg
                
            return response.json()
            
        except Exception as e:
            print(f"Error sending request: {str(e)}\n")
            raise